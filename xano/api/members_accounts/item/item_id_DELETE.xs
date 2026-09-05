// Delete ITEM record.
query "item/{item_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int item_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.item_id
    }
  }

  response = null
  guid = "SkWa3Y3ic_yTfWM4giLDdCKbuYU"
}