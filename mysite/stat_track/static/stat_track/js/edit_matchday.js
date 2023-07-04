// Funkcja do aktualizacji sumy bramek
function updateGoalsSum() {
    var homeGoalsSum = 0;
    var awayGoalsSum = 0;

    // Iteracja przez pola zawodników drużyny domowej
    $("#player-fields-home input[type='number']").each(function () {
        homeGoalsSum += parseInt($(this).val()) || 0;
    });

    // Iteracja przez pola zawodników drużyny wyjazdowej
    $("#player-fields-away input[type='number']").each(function () {
        awayGoalsSum += parseInt($(this).val()) || 0;
    });

    // Aktualizacja sumy bramek w polach home_goals i away_goals
    $("#id_home_goals").val(homeGoalsSum);
    $("#id_away_goals").val(awayGoalsSum);
}

// Event listener dla zmiany drużyny domowej
$("#id_team_home").change(function () {
    const url = $("#matchCreator").attr("data-players-url");
    const team = "home";
    const teamHome = $(this).val();
    const matchdayId = document.getElementById("matchday_id").getAttribute("data-matchday-id");

    $.ajax({
        url: url,
        data: {
            'team': team,
            'team_home': teamHome,
            'matchday_id': matchdayId
        },
        success: function (data) {
            $("#player-fields-home").html(data);
            updateGoalsSum(); // Aktualizacja sumy bramek po zmianie zawodników
        }
    });
});

// Event listener dla zmiany drużyny wyjazdowej
$("#id_team_away").change(function () {
    const url = $("#matchCreator").attr("data-players-url");
    const team = "away";
    const teamAway = $(this).val();
    const matchdayId = document.getElementById("matchday_id").getAttribute("data-matchday-id");

    $.ajax({
        url: url,
        data: {
            'team': team,
            'team_away': teamAway,
            'matchday_id': matchdayId
        },
        success: function (data) {
            $("#player-fields-away").html(data);
            updateGoalsSum(); // Aktualizacja sumy bramek po zmianie zawodników
        }
    });
});

// Event listener dla zmiany wartości pól zawodników drużyny domowej
$("#player-fields-home").on("change", "input[type='number']", function () {
    updateGoalsSum(); // Aktualizacja sumy bramek po zmianie wartości pola
});

// Event listener dla zmiany wartości pól zawodników drużyny wyjazdowej
$("#player-fields-away").on("change", "input[type='number']", function () {
    updateGoalsSum(); // Aktualizacja sumy bramek po zmianie wartości pola
});