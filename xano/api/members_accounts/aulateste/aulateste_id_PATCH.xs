// Edit AulaTeste record
query "aulateste/{aulateste_id}" verb=PATCH {
  api_group = "Members & Accounts"

  input {
    int aulateste_id? filters=min:1
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
      field_value = $input.aulateste_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $model
  }

  response = $model
  guid = "TEge8m8jaf0Tjh7jPTvBgHvv7Gs"
}