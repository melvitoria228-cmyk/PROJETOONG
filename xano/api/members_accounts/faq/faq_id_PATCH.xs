// Edit FAQ record
query "faq/{faq_id}" verb=PATCH {
  api_group = "Members & Accounts"

  input {
    int faq_id? filters=min:1
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
      field_value = $input.faq_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $faq
  }

  response = $faq
  guid = "vLOXaEhK3QP-y_0NdnX787xRm-w"
}