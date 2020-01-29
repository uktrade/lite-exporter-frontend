import requests

from conf.settings import env, STREAMING_CHUNK_SIZE


def get(request, appended_address):
    if request:
        return requests.get(
            env("LITE_API_URL") + appended_address,
            headers={
                "EXPORTER-USER-TOKEN": str(request.user.user_token),
                "X-Correlation-Id": str(request.correlation),
                "ORGANISATION-ID": str(request.user.organisation),
            },
        )

    return requests.get(env("LITE_API_URL") + appended_address)


def post(request, appended_address, json):
    return requests.post(
        env("LITE_API_URL") + appended_address,
        json=json,
        headers={
            "EXPORTER-USER-TOKEN": str(request.user.user_token),
            "X-Correlation-Id": str(request.correlation),
            "ORGANISATION-ID": str(request.user.organisation),
        },
    )


def put(request, appended_address: str, json):
    if not appended_address.endswith("/"):
        appended_address = appended_address + "/"

    return requests.put(
        env("LITE_API_URL") + appended_address,
        json=json,
        headers={
            "EXPORTER-USER-TOKEN": str(request.user.user_token),
            "X-Correlation-Id": str(request.correlation),
            "ORGANISATION-ID": str(request.user.organisation),
        },
    )


def delete(request, appended_address):
    return requests.delete(
        env("LITE_API_URL") + appended_address,
        headers={
            "EXPORTER-USER-TOKEN": str(request.user.user_token),
            "X-Correlation-Id": str(request.correlation),
            "ORGANISATION-ID": str(request.user.organisation),
        },
    )


def read_in_chunks(file):
    """
    Lazy function (generator) to read a file piece by piece.
    """
    while True:
        data = file.read(STREAMING_CHUNK_SIZE)
        if not data:
            break
        yield data


def post_file(request, appended_address, file):
    return requests.post(
        env("LITE_API_URL") + appended_address,
        data={"file": read_in_chunks(file)},
        headers={
            "Content-Disposition": f"attachment; filename={file.name}",
            "EXPORTER-USER-TOKEN": str(request.user.user_token),
            "X-Correlation-Id": str(request.correlation),
            "ORGANISATION-ID": str(request.user.organisation),
        },
    )
