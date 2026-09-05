// Edit ENDERECO record
query "endereco/{endereco_id}" verb=PATCH {
  api_group = "Members & Accounts"

  input {
    int endereco_id? filters=min:1
    dblink {
      table = ""
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch "" {
      field_name = "id"
      field_value = $input.endereco_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $endereco
  }

  response = $endereco
  guid = "5ljK-hjZO9cAUcbVXJ84s-8uKmY"
}