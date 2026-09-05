// Delete STATUS_TESTORNO record.
query "status_testorno/{status_testorno_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int status_testorno_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.status_testorno_id
    }
  }

  response = null
  guid = "JPHNklJre7p79pyPJgYWPsuU9K0"
}