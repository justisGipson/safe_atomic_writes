# SAFE ATOMIC WRITES

with sensitive file writes, trusting a traditional file write can be a huge mistake.

stopping it before the write is completed and synced will, at best, leave us with
corrupt data, & depending on what the file is used for, bigger issues may arise

<br>

what happens in here:

1. - create temp_file in same directory as the file we're trying to create or update. Move operations aren't guaranteed to be atomic when they're between different file systems. Import is set to `delete=False` as the standard behavior of `NamedTemporaryFile` is to delete itself as soon as it's not in use
2. - need to support file creation and updates - initialize temp_file with the target file's contents and metadata
3. - the we write or append the file contents to the temp_file and we flush/sync to disk manually to prep for the replace
4. - `os.replace` is where the magic happens. `os.replace` is an atomic operation (when the source and target are on the same file system), so we're now guaranteed that if this fails to complete, no harm will be done.
5. - use `finally` to remove temp_file in case something did go wrong. but now, worst-case scenario is we have a temp_file.

<br>

```bash
File: sample.json
   1   [
   2       {
   3           "item": "Food_eat",
   4           "Food": {
   5               "foodNo": 42536216,
   6               "type": "fruit",
   7               "moreInfo": [
   8                   "organic"
   9               ]
  10           }
  11       }
  12   ]
```

```bash
 File: sample.yaml
   1   - Food:
   2       foodNo: 42536216
   3       moreInfo:
   4       - organic
   5       type: fruit
   6     item: Food_eat
```
