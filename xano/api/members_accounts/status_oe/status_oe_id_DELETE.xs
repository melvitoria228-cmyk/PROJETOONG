// Delete STATUS_OE record.
query "status_oe/{status_oe_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int status_oe_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.status_oe_id
    }
  }

  response = null
  guid = "9RWVzSA-wm2AmPhUa7l2RysB-Qs"
}