def div_ciel(nominater, denominater):
    if denominater:
        full_pages = nominater // denominater
        additional_page = 1 if nominater % denominater > 0 else 0
        return full_pages + additional_page
    else:  return 1
