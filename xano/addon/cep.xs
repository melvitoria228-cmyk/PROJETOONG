addon CEP {
  input {
    int CEP_id? {
      table = ""
    }
  }

  stack {
    db.query "" {
      where = $db.CEP.id == $input.CEP_id
      return = {type: "single"}
    }
  }

  guid = "Q9kb8VDS3gDsp6HyWD5WnaBo1sU"
}