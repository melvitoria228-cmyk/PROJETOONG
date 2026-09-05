// Delete OP record.
query "op/{op_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int op_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.op_id
    }
  }

  response = null
  guid = "YU_WgpAP95U1p42stTmMISOs2hg"
}