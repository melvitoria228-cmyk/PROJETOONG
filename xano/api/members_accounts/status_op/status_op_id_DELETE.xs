// Delete STATUS_OP record.
query "status_op/{status_op_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int status_op_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.status_op_id
    }
  }

  response = null
  guid = "ZSX8t7w1Vvt3GERKj-GlIP02j-o"
}