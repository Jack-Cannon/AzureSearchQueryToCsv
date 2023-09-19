import csv
import time
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

index_name = "Your index name"
search_service_name = "your service name"
search_dns_suffix = "your dns suffix"
key = "your query key"
search_filter = "your search filter"
select = ["your select list"]

# Get the service endpoint and API key from the environment
endpoint = f"https://{search_service_name}.{search_dns_suffix}"

# Create a client
credential = AzureKeyCredential(key)
client = SearchClient(endpoint=endpoint,
                      index_name=index_name,
                      credential=credential)

results = client.search(search_text="*", include_total_count=True, filter=search_filter, select=select)

print(f"Search Count: {results.get_count()}")

# create columns for csv
field_names = results.next().keys()

print("start writing to csv...")
with open('assets.csv', 'w') as csvfile:
    tic = time.perf_counter()
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(results)
    toc = time.perf_counter()
print(f"Done writing in {toc - tic:0.4f} seconds")
