from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):

    region_name = 'ap-northeast-2'
    location = ''
    bucket_name = 'store-media-server'
    file_overwrite = False
    custom_domain = f's3.{region_name}.amazonaws.com/{bucket_name}'

