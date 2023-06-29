var version = "0.0"

function test(isFlash){
    if(isFlash){
        $("#output").append("<br>")
    }else{
        $("#output").text("")
    }
    $("#output").append("-> Testing ")
    $("#test").text("Testing .. ")
    $("#test").append('<span class="spinner-border spinner-border-sm"></span>')
    timer = setInterval(function () {$("#output").append(".")}, 1e3);
    $.ajax({
        type: "POST",
        url: "/test",
        async: !0,
        data: JSON.stringify({ cmd: "start_test"}),
        success: function (e) {
            clearTimeout(timer)
            if (e.Status == "ok"){
                $("#output").append("<br>")
                $("#output").append("-> The test process was <strong>"+(e.Report)+"</strong>")
                $("#test").text("Start")
            }else{
                $("#output").append("<br>")
                $("#output").append("-> The test process was failed: <br><code>"+e.Report+"</code>")
                $("#test").text("Start")
            }
        },
        error: function () {
            clearTimeout(timer)
            $("#test").text("Start")
            $("#output").append("<br>")
            $("#output").append("-> <span id='success'>"+error+"</span>")
        },
    });
}

function erase_flash(isTest){
    $("#test").text("Flashing .. "),
    $("#output").text(""),
    $("#output").append("-> Erasing and flashing firmware with version: <span id='success'>"+version+"</span> "),
    $("#test").append('<span class="spinner-border spinner-border-sm"></span>'),
    (timer = setInterval(function () {$("#output").append(".")}, 1e3));

    $.ajax({
        type: "POST",
        url: "/test",
        async: !0,
        data: JSON.stringify({ cmd: "start_flashing"}),
        success: function (e) {
            clearTimeout(timer)
            if (e.Status === "ok"){
                $("#output").append("<br>")
                $("#output").append("-> <strong> The erasing and flashing process was successful! </strong>")
                if(isTest){
                    test(true)
                }else{
                    $("#test").text("Start")
                }
            }else{
                $("#test").text("Start")
                $("#output").append("<br>")
                $("#output").append("-> <span id='fail'>"+e.Status+"</span>")
            }
        },
        error: function (xhr, status, error) {
            clearTimeout(timer)
            $("#test").text("Start")
            $("#output").append("<br>")
            $("#output").append("-> <span id='success'>"+error+"</span>")
        },

    });
}

$(function () {
    $("div.mainContainer").load("overview", function () {
        $(".loader").hide(100);
        $.ajax({
            type: "POST",
            url: "/test",
            async: !0,
            data: JSON.stringify({ cmd: "get_firmware_version"}),
            success: function (e) {
                version = e.Status
                testerVersion = e.Tester
                $("#testerVersion").text(testerVersion)
            },
        });
        }
    )
});

$(document).on("click", "#test", function () {
    var isFlash = $("#flashCheckbox").is(":checked")
    var isTest = $("#testCheckbox").is(":checked")


    if($("#test").text() === "Start"){
        if(isFlash == true){
            erase_flash(isTest)
        }else if(isFlash == false && isTest == true){
            test()
        }else if(isFlash == false && isTest == false){
            alert("Zvolte některou z možných procedúr!")
        }
    }
})
$(document).on("click", "#refresh", function () {
    location.reload();
})
