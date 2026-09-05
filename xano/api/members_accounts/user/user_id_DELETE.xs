// Delete user record.
query "user/{user_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int user_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.user_id
    }
  }

  response = null
  guid = "60fbyoffvFSwUF7npQKMbodMoPc"
}