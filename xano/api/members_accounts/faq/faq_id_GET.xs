// Get FAQ record
query "faq/{faq_id}" verb=GET {
  api_group = "Members & Accounts"

  input {
    int faq_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.faq_id
    } as $faq
  
    precondition ($faq != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $faq
  guid = "FhgGFuQSRwwrkMK6LHSTHeVTY8I"
}