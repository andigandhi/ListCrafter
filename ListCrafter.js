base_values = []
depth_factor = [1,5,15,20,50,100]
wordlist = []

year = new Date().getFullYear()

function createWordlist() {
    // Generate the base wordlist 
    getValues()
    wordlist = base_values

    // Add current year to entities of base wordlist
    candidates += combine_strings(base_wordlist, year)

    document.getElementById("output_list").value = wordlist.join("\n")
}


function computeSize() {
    getValues()
    wordlist_length = depth_factor[document.getElementById("list_depth").value] * base_values.length
    document.getElementById("div_length").innerText = "Wordlist will be approximately "+wordlist_length+"entries large"
}


function getValues() {
    // Read all the text fields
    var company = document.getElementById("txt_company").value
    var town = document.getElementById("txt_town").value
    var street = document.getElementById("txt_street").value
    var others = document.getElementById("txt_other").value

    // Add values to the base value array
    base_values = []
    if (company != "") base_values.push(company)
    if (town != "") base_values.push(town)
    if (street != "") base_values.push(street)
    if (others != "") base_values = base_values.concat(others.split(' '))
}

// TODO!
function combine_strings(base_values, append_str) {
    candidates = []
    candidates += append_string_to_list(base_wordlist, append_str)
    candidates += append_string_to_list(base_wordlist, "."+append_str)
    candidates += append_string_to_list(base_wordlist, append_str[2:])
    return candidates
}

// TODO!!
function append_string_to_list(pwlist, string):
    return [s + string for s in pwlist]