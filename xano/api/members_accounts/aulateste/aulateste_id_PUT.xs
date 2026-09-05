// Update AulaTeste record
query "aulateste/{aulateste_id}" verb=PUT {
  api_group = "Members & Accounts"

  input {
    int aulateste_id? filters=min:1
    dblink {
      table = ""
    }
  }

  stack {
    db.edit "" {
      field_name = "id"
      field_value = $input.aulateste_id
      enforce_hidden_fields = false
      data = {status: $input.status}
    } as $model
  }

  response = $model
  guid = "u01ysj7qa5sL4lVHF0oQQ-RFUEM"
}