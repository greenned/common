import os

import pandas as pd
from google.cloud.bigquery import Client
from tqdm import tqdm


def batch_stream_save_from_query(
    bigquery_client: Client,
    query: str,
    output_dir: str,
    page_size: int,
    filename: str,
) -> None:
    # TODO: implement csv, json, avro
    query_job = bigquery_client.query(
        query,
    ).result(page_size=page_size)
    column_headers = [field.name for field in query_job.schema]
    pages = query_job.pages

    total = (
        query_job.total_rows // page_size + 1
        if query_job.total_rows % page_size > 0
        else query_job.total_rows // page_size
    )

    for idx, batch in tqdm(enumerate(pages), total=total, desc=f"save to {output_dir}"):
        batch_values = []
        rows = list(batch)
        for row in rows:
            batch_values.append(row.values())
        batch_values = pd.DataFrame(batch_values, columns=column_headers)
        batch_values.to_parquet(
            os.path.join(output_dir, f"{filename}_{str(idx).zfill(2)}.parquet")
        )
