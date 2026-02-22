"""
Django management command to fetch articles from RSS feeds.

Usage:
    python manage.py fetch_articles
    python manage.py fetch_articles --source 1

This command:
- Fetches all active RSS sources from the database
- Parses their RSS feeds using feedparser
- Creates or updates articles in the database
- Prevents duplicates based on article URL
- Handles encoding issues gracefully
- Logs results to console

Run this command manually or schedule it with cron/celery.
"""
import feedparser
import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from articles.models import Source, Article


class Command(BaseCommand):
    """
    Fetch articles from RSS feeds and save to database.
    """
    help = 'Fetch articles from active RSS feed sources'

    def add_arguments(self, parser):
        """
        Add optional command-line arguments.
        """
        parser.add_argument(
            '--source',
            type=int,
            help='Fetch from specific source ID only',
        )

    def handle(self, *args, **options):
        """
        Main command logic - fetch and process RSS feeds.
        """
        self.stdout.write(self.style.SUCCESS('Starting RSS feed fetch...'))
        
        # Get sources to fetch from
        if options['source']:
            sources = Source.objects.filter(id=options['source'], is_active=True, source_type='RSS')
        else:
            sources = Source.objects.filter(is_active=True, source_type='RSS')
        
        if not sources.exists():
            self.stdout.write(self.style.WARNING('No active RSS sources found.'))
            return
        
        total_fetched = 0
        total_created = 0
        total_updated = 0
        total_skipped = 0
        
        # Process each source
        for source in sources:
            self.stdout.write(f'\nFetching from: {source.name}')
            self.stdout.write(f'  URL: {source.url}')
            
            try:
                # Fetch RSS feed with proper encoding and error handling
                try:
                    response = requests.get(
                        source.url,
                        timeout=30,
                        headers={
                            'User-Agent': 'TechPulse/1.0 (RSS Reader; +https://github.com/matandasoftware/tech-pulse)'
                        }
                    )
                    response.raise_for_status()
                    
                    # Parse the feed (feedparser handles encoding detection)
                    feed = feedparser.parse(response.content)
                    
                except requests.exceptions.Timeout:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Timeout: Feed took too long to respond')
                    )
                    continue
                    
                except requests.exceptions.ConnectionError:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Connection Error: Could not reach feed')
                    )
                    continue
                    
                except requests.exceptions.HTTPError as e:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ HTTP Error: {e.response.status_code}')
                    )
                    continue
                    
                except requests.exceptions.RequestException as e:
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Request Error: {str(e)}')
                    )
                    continue
                
                # Check if feed was parsed successfully
                if feed.bozo and not feed.entries:
                    # Only error if there are NO entries (some feeds have minor bozo warnings)
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Parse Error: {feed.get("bozo_exception", "Unknown error")}')
                    )
                    continue
                
                # Check if feed has entries
                if not feed.entries:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠ No entries found in feed')
                    )
                    continue
                
                self.stdout.write(f'  Found {len(feed.entries)} entries')
                
                # Process each entry in the feed
                entries_created = 0
                entries_updated = 0
                entries_skipped = 0
                
                for entry in feed.entries:
                    total_fetched += 1
                    
                    try:
                        # Extract article data
                        article_data = self.extract_article_data(entry, source)
                        
                        # Skip if no URL (invalid entry)
                        if not article_data.get('url'):
                            entries_skipped += 1
                            total_skipped += 1
                            continue
                        
                        # Create or update article
                        article, created = Article.objects.update_or_create(
                            url=article_data['url'],
                            defaults=article_data
                        )
                        
                        if created:
                            entries_created += 1
                            total_created += 1
                            self.stdout.write(
                                self.style.SUCCESS(f'  ✓ Created: {article.title[:60]}...')
                            )
                        else:
                            entries_updated += 1
                            total_updated += 1
                            self.stdout.write(
                                self.style.WARNING(f'  ↻ Updated: {article.title[:60]}...')
                            )
                    
                    except Exception as e:
                        entries_skipped += 1
                        total_skipped += 1
                        self.stdout.write(
                            self.style.ERROR(f'  ✗ Error processing entry: {str(e)[:50]}')
                        )
                        continue
                
                # Print source summary
                self.stdout.write(
                    f'  Summary: {entries_created} created, {entries_updated} updated, {entries_skipped} skipped'
                )
                
                # Update source last_fetched timestamp
                source.last_fetched = timezone.now()
                source.save()
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Unexpected error: {str(e)}')
                )
        
        # Print overall summary
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS('Fetch complete!'))
        self.stdout.write(f'  Total entries processed: {total_fetched}')
        self.stdout.write(self.style.SUCCESS(f'  ✓ New articles created: {total_created}'))
        self.stdout.write(self.style.WARNING(f'  ↻ Existing articles updated: {total_updated}'))
        if total_skipped > 0:
            self.stdout.write(self.style.ERROR(f'  ✗ Entries skipped: {total_skipped}'))
        self.stdout.write('='*70)

    def detect_category(self, title, content, summary):
        """
        Auto-detect article category based on keywords in title and content.

        Args:
            title: Article title
            content: Article content
            summary: Article summary

        Returns:
            Category object or None
        """
        from articles.models import Category

        # Combine all text for keyword matching (lowercase)
        text = f"{title} {content} {summary}".lower()

        # Define keyword mappings for categories (matching DB category names)
        category_keywords = {
            'Artificial Intelligence': ['artificial intelligence', 'machine learning', 'deep learning', 
                                        'neural network', 'ai', 'gpt', 'chatgpt', 'llm', 'openai', 
                                        'generative', 'cognitive computing', 'ml', 'ai model'],
            'Startups': ['startup', 'startups', 'funding', 'venture capital', 'vc', 'seed round',
                         'series a', 'series b', 'entrepreneur', 'entrepreneurship', 'founder',
                         'unicorn', 'investment', 'investors'],
            'Mobile': ['mobile', 'android', 'ios', 'swift', 'kotlin', 'flutter', 'react native', 
                       'mobile app', 'smartphone', 'iphone', 'samsung', 'app store', 'play store'],
            'Security': ['security', 'cybersecurity', 'hack', 'breach', 'vulnerability', 
                         'encryption', 'malware', 'ransomware', 'firewall', 'privacy', 
                         'data breach', 'cyber attack', 'phishing'],
            'Business': ['business', 'corporate', 'economics', 'finance', 'strategy', 'merger',
                         'acquisition', 'ceo', 'revenue', 'profit', 'market', 'commerce',
                         'enterprise', 'management'],
            'Science': ['science', 'scientific', 'research', 'space', 'physics', 'biology',
                        'chemistry', 'astronomy', 'nasa', 'laboratory', 'study', 'experiment',
                        'discovery', 'quantum'],
            'Software': ['software', 'programming', 'developer', 'coding', 'code', 'framework',
                         'library', 'api', 'web development', 'frontend', 'backend', 'javascript',
                         'python', 'java', 'devops', 'ci/cd', 'github', 'open source'],
            'Technology': ['technology', 'tech', 'innovation', 'digital', 'gadget', 'device',
                          'electronics', 'hardware', 'computing', 'internet', 'web', 'online',
                          'platform', 'service', 'product', 'launch', 'release', 'announcement'],
        }
        # Score each category based on keyword matches
        scores = {}
        for category_name, keywords in category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                scores[category_name] = score

        # If we found matching keywords, return the highest scoring category
        if scores:
            best_category_name = max(scores, key=scores.get)
            try:
                return Category.objects.get(name=best_category_name)
            except Category.DoesNotExist:
                pass

        # Return None if no category matches
        return None

    def extract_article_data(self, entry, source):
        """
        Extract article data from RSS feed entry.

        Args:
            entry: feedparser entry object
            source: Source model instance

        Returns:
            dict: Article data ready for database
        """
        # Get title (required)
        title = entry.get('title', 'No Title').strip()
        if not title:
            title = 'Untitled Article'
        
        # Get URL (required)
        url = entry.get('link', '').strip()
        
        # Get content/summary
        content = ''
        if hasattr(entry, 'content') and entry.content:
            content = entry.content[0].get('value', '')
        elif hasattr(entry, 'description'):
            content = entry.description
        
        # Clean up content (remove extra whitespace)
        content = ' '.join(content.split()) if content else ''
        
        # Get summary (shorter version)
        summary = entry.get('summary', '').strip()
        if not summary and content:
            # Create summary from content (first 200 chars)
            summary = content[:200] + '...' if len(content) > 200 else content
        
        # Get author
        author = entry.get('author', 'Unknown').strip()
        if not author:
            author = 'Unknown'
        
        # Get published date
        published_at = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            try:
                published_at = timezone.datetime(*entry.published_parsed[:6])
                # Make timezone-aware
                if timezone.is_naive(published_at):
                    published_at = timezone.make_aware(published_at)
            except (TypeError, ValueError):
                published_at = timezone.now()
        else:
            published_at = timezone.now()
        
        # Get image URL
        image_url = None
        
        # Try multiple image sources
        if hasattr(entry, 'media_content') and entry.media_content:
            image_url = entry.media_content[0].get('url')
        elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            image_url = entry.media_thumbnail[0].get('url')
        elif hasattr(entry, 'enclosures') and entry.enclosures:
            for enclosure in entry.enclosures:
                if enclosure.get('type', '').startswith('image/'):
                    image_url = enclosure.get('href')
                    break
        
        # Default category (you can make this smarter later)
        category = source.category if hasattr(source, 'category') else None
        
                # Auto-assign category based on keywords
        category = self.detect_category(title, content, summary)
        
        return {
            'title': title[:500],
            'url': url[:500],
            'content': content,
            'summary': summary[:1000] if summary else '',
            'author': author[:200],
            'source': source,
            'category': category,  # ← Now auto-detected!
            'published_at': published_at,
            'image_url': image_url[:500] if image_url else None,
            'fetched_at': timezone.now(),
        }