# Data-related subcommands

## list all data item ids

{{ cli('kiara', 'data', 'list', extra_env={"KIARA_DATA_STORE": "/tmp/data_store_3"}) }}

## get information about a data item

{{ cli('kiara', 'data', 'explain', 'example_table', extra_env={"KIARA_DATA_STORE": "/tmp/data_store_3"}) }}
