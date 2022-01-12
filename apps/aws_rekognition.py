import copy
import io

from PIL import Image
from PIL import ImageDraw, ImageFont
import boto3
import requests


def mark_labels(im: Image, resp: dict, box_color="black"):
    """Mark labels with rectangles on given image in-place.
    """
    width, height = im.size
    fs = height // 30
    # font = ImageFont.truetype("Helvetica", fs)
    draw = ImageDraw.Draw(im)
    LTWH = "Left Top Width Height".split()
    lines = []
    for td in resp["TextDetections"]:
        text = td["DetectedText"]
        conf = td["Confidence"]
        typ = td["Type"]
        if typ == "LINE":
            lines.append(text)
            geom = td["Geometry"]
            bbox = copy.copy(geom["BoundingBox"])
            poly = geom["Polygon"]
            bbox["Left"] *= width
            bbox["Width"] *= width
            bbox["Top"] *= height
            bbox["Height"] *= height
            l, t, w, h = map(int, [bbox[key] for key in LTWH])
            ## draw.text((l, t - fs), text, fill=box_color, font=font)
            draw.rectangle([(l, t), (l + w, t + h)], outline=box_color)
            draw.rectangle([(l-1, t-1), (l + w + 1, t + h + 1)], outline=box_color)
            draw.rectangle([(l-2, t-2), (l + w + 2, t + h + 2)], outline=box_color)


def find_text(
    im,
    aws_access_key_id="",
    aws_secret_access_key="",
    box_color="black"
):
    """Detect text using AWS Rekognition cloud service.
    """
    f = io.BytesIO()
    im.save(f, format="PNG")
    f.seek(0)
    im1 = Image.open(f)

    client = boto3.client(
        "rekognition",
        region_name="us-east-1",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    f.seek(0)
    bytes = f.read()
    resp = client.detect_text(Image={'Bytes': bytes})

    mark_labels(im1, resp, box_color=box_color)
    return resp, im1
