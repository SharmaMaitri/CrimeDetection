function calculateAge() {
    var dob = new Date(document.getElementById("Birthday").value);
    var today = new Date();
    var age = today.getFullYear() - dob.getFullYear();
    var monthDiff = today.getMonth() - dob.getMonth();

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
        age--;
    }
    document.getElementById("Age").value = age;
} 
function eventSubmit() {
    //var Gender = document.querySelector('input[name="gender"]:checked').value;
    var Gender="";
    var NameSet = document.getElementById("NameSet").value;
    var UserName = document.getElementById("UserName").value;
    var Surname = document.getElementById("Surname").value;
    var StreetAddress = document.getElementById("StreetAddress").value;
    var City = document.getElementById("City").value;
    var State = document.getElementById("State").value;
    var ZipCode = document.getElementById("ZipCode").value;
    var EmailAddress = document.getElementById("EmailAddress").value;
    var Area = document.getElementById("Area").value;
    var CountryFull = document.getElementById("CountryFull").value;
    var TelephoneNumber = document.getElementById("TelephoneNumber").value;
    var Birthday = document.getElementById("Birthday").value;
    var Age = document.getElementById("Age").value;
    var Occupation = document.getElementById("Occupation").value;
    var Company = document.getElementById("Company").value;
    var CompanyVehicle = document.getElementById("CompanyVehicle").value;
    var BloodType = document.getElementById("BloodType").value;
    var Kilograms = document.getElementById("Kilograms").value;
    var FeetInches = document.getElementById("FeetInches").value;
    var CrimeType = document.getElementById("CrimeType").value;
    if (document.getElementById('dot-1').checked) {
        Gender=document.getElementById('dot-1').value;
    }
    else if (document.getElementById('dot-2').checked) {
        Gender=document.getElementById('dot-2').value;
    }
    else{
        alert("Please select Gender!!");
        return false;
    }
    if ($('input[name=Gender]:checked').length > 0) {
        window.alert("Please enter a Gender");  
        return false; 
    }
    if (Gender == "" || NameSet == "" || UserName == "" || Surname == "" || StreetAddress == "" || City == "" || State == "" || ZipCode == "" || EmailAddress == "" || Area == ""|| CountryFull == ""|| TelephoneNumber == ""|| Birthday == "" || Age == "" || Occupation == "" || Company == "" || CompanyVehicle == "" || BloodType == "" || Kilograms == "" || FeetInches == "" || CrimeType == "") {
        alert("Please filled out all the fields!!");
        return false;
    } 
    
    if (TelephoneNumber.length == 10) {
        window.alert("Please enter a valid phone number");
        TelephoneNumber.focus();
        return false;
    }
    if (EmailAddress.value == "") {
        window.alert(
          "Please enter a valid e-mail address.");
          EmailAddress.focus();
        return false;
    }
    
    // Send an AJAX request to the Flask app to submit the data
    // var xhr = new XMLHttpRequest();
    // xhr.open("POST", "{{ url_for('addCriminal') }}", true);
    // xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // xhr.onreadystatechange = function() {
    //     if (xhr.readyState === 4 && xhr.status === 200) {
    //         alert(xhr.responseText);
    //     }
    // };
    // xhr.send(JSON.stringify({Gender : Gender ,NameSet: NameSet, UserName: UserName, Surname: Surname, StreetAddress:StreetAddress, City:City, State:State, ZipCode:ZipCode, EmailAddress:EmailAddress, Area:Area, CountryFull:CountryFull, TelephoneNumber:TelephoneNumber, Birthday:Birthday, Age:Age ,Occupation:Occupation,Company:Company, CompanyVehicle:CompanyVehicle, BloodType:BloodType, Kilograms:Kilograms, FeetInches:FeetInches,CrimeType:CrimeType}));
return true;
}
