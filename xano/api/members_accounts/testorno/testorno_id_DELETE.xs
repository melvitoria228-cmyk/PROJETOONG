// Delete TESTORNO record.
query "testorno/{testorno_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int testorno_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.testorno_id
    }
  }

  response = null
  guid = "1GxqTzRzbWaR2YkNb3rSA9NocAQ"
}