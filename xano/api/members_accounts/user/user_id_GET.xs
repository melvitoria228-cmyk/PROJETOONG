// Get user record
query "user/{user_id}" verb=GET {
  api_group = "Members & Accounts"

  input {
    int user_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.user_id
    } as $user
  
    precondition ($user != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $user
  guid = "-HnVG6ct3Tarh0AJ5-7dbkwPRww"
}