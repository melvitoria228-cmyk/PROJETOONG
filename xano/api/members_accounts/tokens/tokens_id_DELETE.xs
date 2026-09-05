// Delete tokens record.
query "tokens/{tokens_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int tokens_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.tokens_id
    }
  }

  response = null
  guid = "tG2vjf4PHG04zq8KRTuxXzTvEK8"
}