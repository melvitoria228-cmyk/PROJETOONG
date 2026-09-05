// Delete FAQ record.
query "faq/{faq_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int faq_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.faq_id
    }
  }

  response = null
  guid = "Bx-Awz2oswDCHr6rxSxqyNsR-H0"
}