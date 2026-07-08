from pricing.models import Product


class DjangoPipeline:
    def process_item(self, item, spider):
        Product.objects.get_or_create(
            name=item.get("name", "Untitled"),
            defaults={
                "url": item.get("url", "https://example.com"),
                "source_site": item.get("source_site", spider.name),
            },
        )
        return item
