"""
Django management command to fetch articles from RSS feeds.

Usage:
    python manage.py fetch_articles

This command:
- Fetches all active RSS sources from the database
- Parses their RSS feeds using feedparser
- Creates or updates articles in the database
- Prevents duplicates based on article URL
- Logs results to console

Run this command manually or schedule it with cron/celery.
"""
import feedparser
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
        
        # Process each source
        for source in sources:
            self.stdout.write(f'\nFetching from: {source.name}')
            
            try:
                # Fetch and parse RSS feed
                feed = feedparser.parse(source.url)
                
                # Check if feed was fetched successfully
                if feed.bozo:
                    self.stdout.write(
                        self.style.ERROR(f'  Error parsing feed: {feed.bozo_exception}')
                    )
                    continue
                
                # Process each entry in the feed
                for entry in feed.entries:
                    total_fetched += 1
                    
                    # Extract article data
                    article_data = self.extract_article_data(entry, source)
                    
                    # Create or update article
                    article, created = Article.objects.update_or_create(
                        url=article_data['url'],
                        defaults=article_data
                    )
                    
                    if created:
                        total_created += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'  ✓ Created: {article.title[:60]}...')
                        )
                    else:
                        total_updated += 1
                        self.stdout.write(
                            self.style.WARNING(f'  ↻ Updated: {article.title[:60]}...')
                        )
                
                # Update source last_fetched timestamp
                source.last_fetched = timezone.now()
                source.save()
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  Error fetching {source.name}: {str(e)}')
                )
        
        # Print summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'Fetch complete!'))
        self.stdout.write(f'  Total entries processed: {total_fetched}')
        self.stdout.write(self.style.SUCCESS(f'  New articles created: {total_created}'))
        self.stdout.write(self.style.WARNING(f'  Existing articles updated: {total_updated}'))
        self.stdout.write('='*60)

    def extract_article_data(self, entry, source):
        """
        Extract article data from RSS feed entry.
        
        Args:
            entry: feedparser entry object
            source: Source model instance
            
        Returns:
            dict: Article data ready for database
        """
        # Get title
        title = entry.get('title', 'No Title')
        
        # Get URL
        url = entry.get('link', '')
        
        # Get content/summary
        content = ''
        if hasattr(entry, 'content'):
            content = entry.content[0].value
        elif hasattr(entry, 'description'):
            content = entry.description
        
        # Get summary (shorter version)
        summary = entry.get('summary', '')
        if not summary and content:
            # Create summary from content (first 200 chars)
            summary = content[:200] + '...' if len(content) > 200 else content
        
        # Get author
        author = entry.get('author', 'Unknown')
        
        # Get published date
        published_at = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            published_at = timezone.datetime(*entry.published_parsed[:6])
            # Make timezone-aware
            if timezone.is_naive(published_at):
                published_at = timezone.make_aware(published_at)
        else:
            published_at = timezone.now()
        
        # Get image URL
        image_url = None
        if hasattr(entry, 'media_content') and entry.media_content:
            image_url = entry.media_content[0].get('url')
        elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            image_url = entry.media_thumbnail[0].get('url')
        
        # Default category (you can make this smarter later)
        category = source.category if hasattr(source, 'category') else None
        
        return {
            'title': title,
            'url': url,
            'content': content,
            'summary': summary,
            'author': author,
            'source': source,
            'category': category,
            'published_at': published_at,
            'image_url': image_url,
            'fetched_at': timezone.now(),
        }