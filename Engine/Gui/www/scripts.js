// document.getElementById('imgVesselPressure').innerHTML = ""
// import fs from "fs";

async function getPathToFile() {
    var dosya_path = await eel.btn_ResimyoluClick()();
    // var html = [
    //     '<div class="path" id="test">',
    //     '<p>' + dosya_path[0] + '</p>',
    // '</div>'
    //
    // ].join('\n')
        var string =""
        for (var i=0; i< dosya_path.length; i++)
        {
            dosya_path[i] = dosya_path[i] + '<br />';
            string+= dosya_path[i]
        }

        // dosya_path.replace(",","<br />");
    document.getElementById('files').innerHTML = string
    // if (dosya_path) {
    // console.log(dosya_path);
    //                 }
                                }
    function deleteFiles(){
    document.getElementById('files').innerHTML = ""
        eel.earseData();

    }

// src = "eel.js"
// <script src="eel.js"></script>

    // function get_input_directory(){
    // var data = document.getElementById("files").va
    // eel.get_input(data)
    //                                 }
    // import * as inj from './classes'
    // eel.expose(send_img)
    // function send_img(){
    //
    // var img = '/img/sim_plot_0.png'
    // var html = [
    // '<div class="uicomponent-panel-controls-container">',
    // '<img src=' + img + '>',
    // '</div>'
    // ].join('\n');
    // document.getElementById('img').innerHTML = html
    //
    //                     }
    eel.expose(manage_images)
    function manage_images(images){
    document.getElementById("logs").innerHTML = ""
         // var images =['/img/sim_plot_0.png']
    // var images = fs.readdirSync('/img'
    //     console.log(images)
    var container = document.getElementById('img');
    container.innerHTML =''

    for (var i = 0; i < images.length; i++) {
    // create the image element
    var imageElement = document.createElement('img');
    imageElement.setAttribute('src', images[i]);

    // append the element to the container
    //     var br = document.createElement('/')
    // imageElement.appendChild(br)
    container.appendChild(imageElement);

     //
     //    // imageElement.appendChild(br)
     //    if (i==1){
     //           container.insertBefore(br,imageElement )
     //    }


    }
    // console.log(container)
    }

    function callPython(){
    var time = document.getElementById("simulationTime").value
    var  inj_hole_diam= document.getElementById("injectorHoleDiameter").value
    var  inj_hole_num= document.getElementById("injectorHolesNumber").value
    var  inj_kloss= document.getElementById("injectorKLoss").value
    var  nozzle_throat_diam= document.getElementById("nozzleThroatDiameter").value
    var  nozzle_exit_diam= document.getElementById("nozzleExitDiameter").value
    var  eff = document.getElementById("realCoefficient").value
    var  ves_press= document.getElementById("vesselPressure").value
    var  ves_vol= document.getElementById("vesselVolume").value
    var  oxid_mass= document.getElementById("oxidizerMass").value
    var  fuel_len= document.getElementById("fuelLength").value
    var  fuel_dens= document.getElementById("fuelDensity").value
    var  c_a= document.getElementById("ballisticCoefficientA").value
    var  c_n= document.getElementById("ballisticCoefficientN").value
    var  oxid_name= document.getElementById("oxidizerName").value
    var  oxid_form= document.getElementById("oxidizerFormula").value
    var  oxid_temp= document.getElementById("oxidizerTemperature").value
    var  oxid_enth= document.getElementById("oxidizerEnthalpy").value
    var  fuel_name= document.getElementById("fuelName").value
    var  fuel_form= document.getElementById("fuelFormula").value
    var  fuel_temp= document.getElementById("fuelTemperature").value
    var  fuel_enth= document.getElementById("fuelEnthalpy").value
    var  fuel_port_diam= document.getElementById("fuelPortDiameter").value

    // eel.checkbox(checkbox_1)
    // eel.catch_checkboxes(send_checkboxes())
    var engine = {
        'Injector': [inj_hole_num, inj_hole_diam, inj_kloss],
        'Nozzle': [nozzle_exit_diam, nozzle_throat_diam, eff],
        'Vessel': [ves_press, ves_vol, oxid_mass],
        'Fuel': [fuel_temp, fuel_enth, fuel_name, fuel_form,fuel_port_diam, fuel_len, fuel_dens, c_a, c_n],
        'Oxidizer': [oxid_temp, oxid_enth, oxid_name, oxid_form]

    }

    // eel.injector(inj_hole_num, inj_hole_diam, inj_kloss)
    // eel.nozzle(nozzle_exit_diam, nozzle_throat_diam, eff)
    // eel.vessel(ves_press, ves_vol, oxid_mass)
    // eel.fuel(fuel_temp, fuel_enth, fuel_name, fuel_form,fuel_port_diam, fuel_len, fuel_dens, c_a, c_n )
    // eel.oxid(oxid_temp, oxid_enth, oxid_name, oxid_form)
    // eel.rest(time, eff)
    // eel.save_cache(time)
    eel.run(send_checkboxes(),time, engine)


}


function send_checkboxes(){

   var dict_1 = {
        'thrust': document.getElementById("plotThrust").checked,
        'pressure_vessel': document.getElementById("plotVesselPressure").checked,
        'pressure_chamber': document.getElementById("plotChamberPressure").checked,
        'isp': document.getElementById("plotIsp").checked,
        'of': document.getElementById("plotOF").checked,
        'oxid_mass_flow': document.getElementById("plotOxidizerFlow").checked,
        'fuel_mass_flow': document.getElementById("plotFuelFlow").checked,
        'diam_port': document.getElementById("plotFuelPortDiameter").checked,
        'gox': document.getElementById("flowGox").checked,
        'temperature': document.getElementById('plotTemperature').checked

    }
    var dict_2 = {
        'allPressures': document.getElementById("allPressures").checked,
        'allMassFlows': document.getElementById("allMassFlows").checked,
        'realAndSimulated': document.getElementById("realAndSimulated").checked,
        'equilibrium': document.getElementById('equilibrium').checked,
        'compareWithPrevious': document.getElementById('compareWithPrevious').checked
    }
    return [dict_1, dict_2]







}

// var input = document.getElementById("head");
// input.addEventListener("keyup", function (event){
//     if (event.keyCode === 13){
//         event.preventDefault();
//         document.getElementById("submit").click()
//     }
// })

document.addEventListener("keyup", function(evnt){

    if (evnt.keyCode === 13)
     {
       document.getElementById("submit").click()
     }
});
eel.expose(sendLogs)
function sendLogs(logs){
    document.getElementById('img').innerHTML = ""
    document.getElementById("logs").innerHTML = logs

}
  // document.onkeyup(function (event){
  //       if(event.keyCode === 13){
  //               document.getElementById("submit").click()
  //       }
  //   })

