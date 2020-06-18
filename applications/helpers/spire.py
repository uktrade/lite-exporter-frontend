import directory_client_core.base

from django.conf import settings


class SpireClient(directory_client_core.base.AbstractAPIClient):
    version = 1  # AbstractAPIClient exposes this in UserAgent header

    def list_licenses(self, **params):
        return self.get("/api/spire/licence/", params=params)

    def get_license(self, pk):
        return self.get(f"/api/spire/licence/{pk}/")


client = SpireClient(
    base_url=settings.LITE_SPIRE_ARCHIVE_CLIENT_BASE_URL,
    api_key=settings.LITE_SPIRE_ARCHIVE_CLIENT_HAWK_SECRET,
    sender_id=settings.LITE_SPIRE_ARCHIVE_CLIENT_HAWK_SENDER_ID,
    timeout=settings.LITE_SPIRE_ARCHIVE_CLIENT_DEFAULT_TIMEOUT,
)
