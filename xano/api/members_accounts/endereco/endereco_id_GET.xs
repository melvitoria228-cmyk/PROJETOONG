// Get ENDERECO record
query "endereco/{endereco_id}" verb=GET {
  api_group = "Members & Accounts"

  input {
    int endereco_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.endereco_id
    } as $endereco
  
    precondition ($endereco != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $endereco
  guid = "gF0wf7TfeUhHDaCyTEej2KPRyU0"
}