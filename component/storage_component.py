from google.cloud import storage
from google.cloud import exceptions
import logging
import sys
# from google.cloud import storage

class StorageComponent(object):
    """
    Class to create  GCP Storage client and related methods

    Attributes:
        storage_client (String): Description

    """

    def __init__(self):
        """
        Constructor to initialize project related parameters
        """
        self.storage_client = self.get_storage_client()

    def get_storage_client(self):
        """
        Method to create a storage client


        Returns:
                storage client object
        """
        try:

            client = storage.Client()
            logging.info("Creating storage client")
            return client
        except Exception as e:
            print("An Unknown exception {} has occurred, requires manual intervention".format(e))
            #logging.error(e)
            sys.exit()

    def create_bucket(self, bucket_name):
        """
        Creates a new bucket with the given bucket_name

        Arguments:
            bucket_name (String): desired name for bucket
        Raises:
            Conflict: if bucket to be created already exists
        """
        #storage_client = self.storage_client
        try:
            bucket = self.storage_client.create_bucket(bucket_name)
            print('Bucket {} created'.format(bucket.name))
        except exceptions.Conflict as e:
            # handling if bucket already exists
            print('Bucket already exists. Returning !!')
        except Exception as e:
            print("An Unknown exception {} has occurred, requires manual intervention" .format(e))
            #logging.error(e)
            sys.exit()

    def delete_bucket(self, bucket_name):
        """Deletes a bucket. The bucket must be empty.

        Args:
            bucket_name (String): Name of the bucket
        Raises:
            NotFound: If the bucket name does not exist
        """
        #storage_client = self.storage_client
        try:
            bucket = self.storage_client.get_bucket(bucket_name)
            bucket.delete()
            print('Bucket {} deleted'.format(bucket.name))
        except exceptions.NotFound as e:
            # Bucket does not exist
            print('Bucket does not exist!, Please recheck the bucket name')
        except Exception as e:
            print("An Unknown exception {} has occurred, requires manual intervention" .format(e))
            #logging.error(e)
            sys.exit()

    def list_files(self, bucket_name):
        """Lists all the files in the bucket.

        Args:
            bucket_name (String): Name of the bucket
        Raises:
            NotFound: If the bucket name does not exist
        """
        #storage_client = self.storage_client
        try:
            bucket = self.storage_client.get_bucket(bucket_name)

            blobs = bucket.list_blobs()

            for blob in blobs:
                print(blob.name)
        except exceptions.NotFound as e:
            # Bucket does not exist
            print('Bucket does not exist!, Please recheck the bucket name')
        except Exception as e:
            print("An Unknown exception {} has occurred, requires manual intervention" .format(e))
            #logging.error(e)
            sys.exit()


            
    def upload_blob(self,bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        # bucket_name = "your-bucket-name"
        # source_file_name = "local/path/to/file"
        # destination_blob_name = "storage-object-name"
        try:

            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)

            print(
                "File {} uploaded to {}.".format(
                    source_file_name, destination_blob_name
                )
            )
        except Exception as e:
            print("An Unknown exception {} has occurred, requires manual intervention" .format(e))
            #logging.error(e)
            sys.exit()
