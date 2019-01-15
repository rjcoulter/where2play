var dayDict = {}
var data = {}
var court = ''
var facility = ''
var days = 0
var date = ''
var json_list = {}
var aJson_list = {}

function calculateHours(startTime, endTime) {
    var tempHours = endTime - startTime;

    if (tempHours > 0) {
        return tempHours;
    }

    return (24 + tempHours);
}

function militaryToNormal(militaryTime) {
    ending = ' AM';

    if (12 <= militaryTime && militaryTime < 24) {
        ending = ' PM';
    }

    if (militaryTime % 12 == 0) {
        return 12 + ending;
    }

    return militaryTime % 12 + ending;
}

function getDate(date) {
    var arr = date.split('/');
    return new Date(arr[2], arr[0] - 1, arr[1]);
}

function createTable(startTime, endTime, date, days, court, facility, times, aTimes, court_availability) {
    var weekday = new Array(7);
    weekday[0] = "Sun.";
    weekday[1] = "Mon.";
    weekday[2] = "Tues.";
    weekday[3] = "Weds.";
    weekday[4] = "Thurs.";
    weekday[5] = "Fri.";
    weekday[6] = "Sat.";

    var month = new Array(12);
    month[0] = 'Jan';
    month[1] = 'Feb';
    month[2] = 'Mar';
    month[3] = 'Apr';
    month[4] = 'May';
    month[5] = 'Jun';
    month[6] = 'Jul';
    month[7] = 'Aug';
    month[8] = 'Sept';
    month[9] = 'Oct';
    month[10] = 'Nov';
    month[11] = 'Dec';

    var result = window.csrf_token.match(/([A-Za-z0-9]){64}/);
    var token = result[0];

    date = date
    days = days
    court = court
    facility = facility
    json_list = times
    aJson_list = aTimes

    var hours = calculateHours(startTime, endTime);
    var d = getDate(date);
    var theader = '<table cellpadding="0" cellspacing="0" id="user_schedule">\n';
    var tSheader = '<table cellpadding="0" cellspacing="0" id="availability_schedule">\n';
    var tbody = '';
    var tsbody = '';

    var hourCounter = 0;

    for (var i = 0; i < hours + 1; i++) {
        if (i == 0) {
            tbody += '<tr><td class="noselect date time"></td>';
            tsbody += '<tr><td class="noselect date time"></td>';
            for (var j = 0; j < days; j++) {
                dayDict[j] = d.getFullYear() + '-' + d.getMonth() + '-' + d.getDate();
                data[d.getFullYear() + '-' + d.getMonth() + '-' + d.getDate()] = []
                tbody += '<td class="noselect date time">' + weekday[d.getDay()] + ' ' + month[d.getMonth()] + ' ' + d.getDate() + '</td>';
                tsbody += '<td class="noselect date time">' + weekday[d.getDay()] + ' ' + month[d.getMonth()] + ' ' + d.getDate() + '</td>';
                d.setDate(d.getDate() + 1);
            }
            tbody += '</tr>\n';
            tsbody += '</tr>\n';
            d.setDate(d.getDate() - days)
        } else {
            tbody += '<tr id="' + parseInt((startTime + hourCounter) * 100) + '">';
            tsbody += '<tr>';
            for (var j = 0; j < days; j++) {
                var gridMonth = d.getMonth() + 1
                if (gridMonth < 10) {
                    gridMonth = "0" + gridMonth
                }
                var gridDate = parseInt(d.getDate())
                if (gridDate < 10) {
                    gridDate = "0" + gridDate
                }
                var gridTime = parseInt((startTime + hourCounter) * 100)
                if (gridTime < 1000) {
                    gridTime = '0' + gridTime
                }
                var gridYear = d.getFullYear()
                if (j == 0) {
                    var date = gridYear + '-' + gridMonth + '-' + gridDate
                    var time = gridTime.toString()

                    if (date in court_availability && court_availability[date][time] === false) {
                        tbody += '<td class="noselect time">' + militaryToNormal(parseInt(startTime + hourCounter)) + '</td><td class="noselect availability full_hour black" id="' + gridMonth + '/' + gridDate + '/' + gridYear + ' ' + gridTime + '"></td>'
                    } else if ((date in times) && (times[date]).includes(time)) {
                        tbody += '<td class="noselect time">' + militaryToNormal(parseInt(startTime + hourCounter)) + '</td><td class="noselect availability full_hour highlighted9" id="' + gridMonth + '/' + gridDate + '/' + gridYear + ' ' + gridTime + '"></td>'
                    } else {
                        tbody += '<td class="noselect time">' + militaryToNormal(parseInt(startTime + hourCounter)) + '</td><td class="noselect availability full_hour" id="' + gridMonth + '/' + gridDate + '/' + gridYear + ' ' + gridTime + '"></td>'
                    }

                    if (date in court_availability && court_availability[date][time] === false) {
                        tsbody += '<td class="noselect time">' + militaryToNormal(parseInt(startTime + hourCounter)) + '</td><td class="noselect availability full_hour black"></td>';
                    } else if (date in aTimes && aTimes[date][time] != 0) {
                        var counter = aTimes[date][time];
                        if (counter > 9) {
                            counter = 9
                        }

                        tsbody += '<td class="noselect time">' + militaryToNormal(parseInt(startTime + hourCounter)) + '</td><td class="noselect availability full_hour highlighted' + counter.toString() + '"></td>';
                    } else {
                        tsbody += '<td class="noselect time">' + militaryToNormal(parseInt(startTime + hourCounter)) + '</td><td class="noselect availability full_hour"></td>';
                    }

                    d.setDate(d.getDate() + 1)
                } else {
                    var date = gridYear + '-' + gridMonth + '-' + gridDate
                    var time = gridTime.toString()

                    if (date in court_availability && court_availability[date][time] === false) {
                        tbody += '</td><td class="noselect availability full_hour black" id="' + gridMonth + '/' + gridDate + '/' + gridYear + ' ' + gridTime + '"></td>';
                    } else if ((date in times) && (times[date].includes(time))) {
                        tbody += '</td><td class="noselect availability full_hour highlighted9" id="' + gridMonth + '/' + gridDate + '/' + gridYear + ' ' + gridTime + '"></td>';
                    } else {
                        tbody += '</td><td class="noselect availability full_hour" id="' + gridMonth + '/' + gridDate + '/' + gridYear + ' ' + gridTime + '"></td>';
                    }

                    if (date in court_availability && court_availability[date][time] === false) {
                        tsbody += '</td><td class="noselect availability full_hour black"></td>';
                    } else if (date in aTimes && aTimes[date][time] != 0) {
                        var counter = aTimes[date][time];
                        if (counter > 9) {
                            counter = 9
                        }

                        tsbody += '</td><td class="noselect availability full_hour highlighted' + counter.toString() + '"></td>';
                    } else {
                        tsbody += '</td><td class="noselect availability full_hour"></td>';
                    }

                    d.setDate(d.getDate() + 1)
                }
            }
            d.setDate(d.getDate() - days)

            tbody += '</tr>\n';
            tsbody += '</tr>\n';

            tbody += '<tr id="' + parseInt((startTime + hourCounter) * 100 + 30) + '">';
            tsbody += '<tr>';
            for (var j = 0; j < days; j++) {
                var gridMonth = d.getMonth() + 1
                if (gridMonth < 10) {
                    gridMonth = "0" + gridMonth
                }
                var gridDate = parseInt(d.getDate())
                if (gridDate < 10) {
                    gridDate = "0" + gridDate
                }
                var gridYear = d.getFullYear()
                var gridTime = parseInt((startTime + hourCounter) * 100 + 30)
                if (gridTime < 1000) {
                    gridTime = '0' + gridTime
                }
                if (j == 0) {
                    var date = gridYear + '-' + gridMonth + '-' + gridDate
                    var time = gridTime.toString()

                    if (date in court_availability && court_availability[date][time] === false) {
                        tbody += '<td class="noselect time"></td><td class="noselect availability half_hour black" id="' + gridMonth + '/' + gridDate + '/' + gridYear + ' ' + gridTime + '"></td>'
                    } else if ((date in times) && (times[date]).includes(time)) {
                        tbody += '<td class="noselect time"></td><td class="noselect availability half_hour highlighted9" id="' + gridMonth + '/' + gridDate + '/' + gridYear + ' ' + gridTime + '"></td>'
                    } else {
                        tbody += '<td class="noselect time"></td><td class="noselect availability half_hour" id="' + gridMonth + '/' + gridDate + '/' + gridYear + ' ' + gridTime + '"></td>'
                    }

                    if (date in court_availability && court_availability[date][time] === false) {
                        tsbody += '<td class="noselect time"></td><td class="noselect availability half_hour black"></td>';
                    } else if (date in aTimes && aTimes[date][time] != 0) {
                        var counter = aTimes[date][time];
                        if (counter > 9) {
                            counter = 9
                        }

                        tsbody += '<td class="noselect time"></td><td class="noselect availability half_hour highlighted' + counter.toString() + '"></td>';
                    } else {
                        tsbody += '<td class="noselect time"></td><td class="noselect availability half_hour"></td>'
                    }

                    d.setDate(d.getDate() + 1)
                } else {
                    var date = gridYear + '-' + gridMonth + '-' + gridDate
                    var time = gridTime.toString()

                    if (date in court_availability && court_availability[date][time] === false) {
                        tbody += '<td class="noselect availability half_hour black" id="' + gridMonth + '/' + gridDate + '/' + gridYear + ' ' + gridTime + '"></td>'
                    } else if ((date in times) && (times[date].includes(time))) {
                        tbody += '<td class="noselect availability half_hour highlighted9" id="' + gridMonth + '/' + gridDate + '/' + gridYear + ' ' + gridTime + '"></td>'
                    } else {
                        tbody += '<td class="noselect availability half_hour" id="' + gridMonth + '/' + gridDate + '/' + gridYear + ' ' + gridTime + '"></td>'
                    }

                    if (date in court_availability && court_availability[date][time] === false) {
                        tsbody += '<td class="noselect availability half_hour highlighted"></td>';
                    } else if (date in aTimes && aTimes[date][time] != 0) {
                        var counter = aTimes[date][time];
                        if (counter > 9) {
                            counter = 9
                        }

                        tsbody += '<td class="noselect availability half_hour highlighted' + counter.toString() + '"></td>';
                    } else {
                        tsbody += '<td class="noselect availability half_hour"></td>'
                    }

                    d.setDate(d.getDate() + 1)
                }
            }
            d.setDate(d.getDate() - days)
            tbody += '</tr>\n';
            tsbody += '</tr>\n';

            hourCounter += 1;
        }
    }

    var tfooter = '</table>';
    var tsfooter = '</table>';

    document.getElementById('user_table_container').innerHTML = theader + tbody + tfooter;
    document.getElementById('availability_table_container').innerHTML = tSheader + tsbody + tsfooter;
}

function getHighlightedCells() {
    var selected = document.getElementsByClassName('highlighted9');
    var tempData = JSON.parse(JSON.stringify(data));

    console.log(data)

    for (var i = 0; i < selected.length; i++) {
        tempData[dayDict[selected[i].cellIndex - 1]].push(selected[i].closest('tr').id);
    }

    var result = window.csrf_token.match(/([A-Za-z0-9]){64}/);
    var token = result[0];

    fetch('/signUpForTimes/', {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            "X-CSRFToken": token,
        },
        body: JSON.stringify({
            times: tempData,
            court: court,
            facility: facility,
            days: days,
            date: date,
            json_list: json_list,
            aJson_list: aJson_list
        })
    }).then(
        response => response.text()
    )
}

function createAvailabilityTable(startTime, endTime, date, days, court, facility, aTimes) {
    var weekday = new Array(7);
    weekday[0] = "Sun.";
    weekday[1] = "Mon.";
    weekday[2] = "Tues.";
    weekday[3] = "Weds.";
    weekday[4] = "Thurs.";
    weekday[5] = "Fri.";
    weekday[6] = "Sat.";

    var month = new Array(12);
    month[0] = 'Jan';
    month[1] = 'Feb';
    month[2] = 'Mar';
    month[3] = 'Apr';
    month[4] = 'May';
    month[5] = 'Jun';
    month[6] = 'Jul';
    month[7] = 'Aug';
    month[8] = 'Sept';
    month[9] = 'Oct';
    month[10] = 'Nov';
    month[11] = 'Dec';

    var result = window.csrf_token.match(/([A-Za-z0-9]){64}/);
    var token = result[0];

    date = date
    days = days
    court = court
    facility = facility
    aJson_list = aTimes

    var hours = calculateHours(startTime, endTime);
    var d = getDate(date);
    var tSheader = '<table cellpadding="0" cellspacing="0" id="availability_schedule">\n';
    var tsbody = '';

    var hourCounter = 0;

    for (var i = 0; i < hours + 1; i++) {
        if (i == 0) {
            tsbody += '<tr><td class="noselect date time"></td>';
            for (var j = 0; j < days; j++) {
                dayDict[j] = d.getFullYear() + '-' + d.getMonth() + '-' + d.getDate();
                data[d.getFullYear() + '-' + d.getMonth() + '-' + d.getDate()] = []
                tsbody += '<td class="noselect date time">' + weekday[d.getDay()] + ' ' + month[d.getMonth()] + ' ' + d.getDate() + '</td>';
                d.setDate(d.getDate() + 1);
            }
            tsbody += '</tr>\n';
            d.setDate(d.getDate() - days)
        } else {
            tsbody += '<tr>';
            for (var j = 0; j < days; j++) {
                var gridMonth = d.getMonth() + 1
                if (gridMonth < 10) {
                    gridMonth = "0" + gridMonth
                }
                var gridDate = parseInt(d.getDate())
                if (gridDate < 10) {
                    gridDate = "0" + gridDate
                }
                var gridTime = parseInt((startTime + hourCounter) * 100)
                if (gridTime < 1000) {
                    gridTime = '0' + gridTime
                }
                var gridYear = d.getFullYear()
                if (j == 0) {
                    var date = gridYear + '-' + gridMonth + '-' + gridDate
                    var time = gridTime.toString()

                    if (date in aTimes && aTimes[date][time] != 0) {
                        var counter = aTimes[date][time];
                        if (counter > 9) {
                            counter = 9
                        }

                        tsbody += '<td class="noselect time">' + militaryToNormal(parseInt(startTime + hourCounter)) + '</td><td class="noselect availability full_hour highlighted' + counter.toString() + '"></td>';
                    } else {
                        tsbody += '<td class="noselect time">' + militaryToNormal(parseInt(startTime + hourCounter)) + '</td><td class="noselect availability full_hour"></td>';
                    }

                    d.setDate(d.getDate() + 1)
                } else {
                    var date = gridYear + '-' + gridMonth + '-' + gridDate
                    var time = gridTime.toString()

                    if (date in aTimes && aTimes[date][time] != 0) {
                        var counter = aTimes[date][time];
                        if (counter > 9) {
                            counter = 9
                        }

                        tsbody += '</td><td class="noselect availability full_hour highlighted' + counter.toString() + '"></td>';
                    } else {
                        tsbody += '</td><td class="noselect availability full_hour"></td>';
                    }

                    d.setDate(d.getDate() + 1)
                }
            }
            d.setDate(d.getDate() - days)

            tsbody += '</tr>\n';

            tsbody += '<tr>';
            for (var j = 0; j < days; j++) {
                var gridMonth = d.getMonth() + 1
                if (gridMonth < 10) {
                    gridMonth = "0" + gridMonth
                }
                var gridDate = parseInt(d.getDate())
                if (gridDate < 10) {
                    gridDate = "0" + gridDate
                }
                var gridYear = d.getFullYear()
                var gridTime = parseInt((startTime + hourCounter) * 100 + 30)
                if (gridTime < 1000) {
                    gridTime = '0' + gridTime
                }
                if (j == 0) {
                    var date = gridYear + '-' + gridMonth + '-' + gridDate
                    var time = gridTime.toString()

                    if (date in aTimes && aTimes[date][time] != 0) {
                        var counter = aTimes[date][time];
                        if (counter > 9) {
                            counter = 9
                        }

                        tsbody += '<td class="noselect time"></td><td class="noselect availability half_hour highlighted' + counter.toString() + '"></td>';
                    } else {
                        tsbody += '<td class="noselect time"></td><td class="noselect availability half_hour"></td>'
                    }

                    d.setDate(d.getDate() + 1)
                } else {
                    var date = gridYear + '-' + gridMonth + '-' + gridDate
                    var time = gridTime.toString()

                    if (date in aTimes && aTimes[date][time] != 0) {
                        var counter = aTimes[date][time];
                        if (counter > 9) {
                            counter = 9
                        }

                        tsbody += '<td class="noselect availability half_hour highlighted' + counter.toString() + '"></td>';
                    } else {
                        tsbody += '<td class="noselect availability half_hour"></td>'
                    }

                    d.setDate(d.getDate() + 1)
                }
            }
            d.setDate(d.getDate() - days)
            tsbody += '</tr>\n';

            hourCounter += 1;
        }
    }

    var tsfooter = '</table>';

    document.getElementById('availability_table_container').innerHTML = tSheader + tsbody + tsfooter;
}

$(function () {
    let colors = ["highlighted1", "highlighted2", "highlighted3", "highlighted4", "highlighted5", "highlighted6", "highlighted7", "highlighted8", "highlighted9"]
    var isMouseDown = false;
    var isMouseDown1 = false;
    var hasSpace = true;

    $("#user_schedule td.availability")
        .mousedown(function () {
            isMouseDown1 = true
            if ($(this).html() == " ") {
                $(this).toggleClass("highlighted9")
                hasSpace = false
                $(this).html("")
            }
            else {
                $(this).toggleClass("highlighted9")
                hasSpace = true
                $(this).html(" ")
            }
            return false; // prevent text selection
        })
        .mouseover(function () {
            if (isMouseDown1 && !hasSpace && $(this).html() == " ") {
                $(this).toggleClass("highlighted9")
                $(this).html("")
            }
            if (isMouseDown1 && hasSpace && $(this).html() == "") {
                $(this).toggleClass("highlighted9")
                $(this).html(" ")
            }
        })
        .mouseup(function () {
            getHighlightedCells()
        });

    $(document)
        .mouseup(function () {
            isMouseDown1 = false;
        });
});

$(document).ready(function () {
    $("a.submit").click(function () {
        document.getElementById("availability_form").submit();
    });
});