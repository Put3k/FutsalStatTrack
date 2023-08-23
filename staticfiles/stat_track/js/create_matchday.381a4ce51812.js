// Adding Players to teams in edit_matchday
$(document).ready(function() {
    //Blue Team button
    $("#add_to_blue").click(function() {
        $("#available_players option:selected").each(function() {
            $(this).removeClass("orange colors").addClass("blue");
            $('<span class="color-box blue"></span>').insertBefore($(this));
            $(this).appendTo("#team_blue").attr("data-team", "blue");
        });
        $("#blue_count").text($("#team_blue option").length);
    });

    //Orange Team button
    $("#add_to_orange").click(function() {
        $("#available_players option:selected").each(function() {
            $(this).removeClass("blue colors").addClass("orange");
            $('<span class="color-box orange"></span>').insertBefore($(this));
            $(this).appendTo("#team_orange").attr("data-team", "orange");
        });
        $("#orange_count").text($("#team_orange option").length);
    });

    //Colors Team button
    $("#add_to_colors").click(function() {
        $("#available_players option:selected").each(function() {
            $(this).removeClass("blue orange").addClass("colors");
            $('<span class="color-box green"></span>').insertBefore($(this));
            $(this).appendTo("#team_colors").attr("data-team", "colors");
        });
        $("#colors_count").text($("#team_colors option").length);
    });

    //Remove from Blue team
    $("#remove_player_blue").click(function() {
        $("#team_blue option:selected").each(function() {
            $(this).prev(".color-box").remove();
            $(this).appendTo("#available_players").removeClass("blue orange colors");
        });
        $("#blue_count").text($("#team_blue option").length);
    });

    //Remove from Orange team
    $("#remove_player_orange").click(function() {
        $("#team_orange option:selected").each(function() {
            $(this).prev(".color-box").remove();
            $(this).appendTo("#available_players").removeClass("blue orange colors");
        });
        $("#orange_count").text($("#team_orange option").length);
    });

    //Remove from Colors team
    $("#remove_player_colors").click(function() {
        $("#team_colors option:selected").each(function() {
            $(this).prev(".color-box").remove();
            $(this).appendTo("#available_players").removeClass("blue orange colors");
        });
        $("#colors_count").text($("#team_colors option").length);
    });
});


//Searchbar for Availalbe players
document.addEventListener('DOMContentLoaded', function () {
  var input = document.getElementById('player-name-input');
  var options = document.getElementById('available_players').options;

  input.addEventListener('input', function () {
    var inputValue = this.value.toLowerCase();

    for (var i = 0; i < options.length; i++) {
      var playerName = options[i].textContent.toLowerCase();
      if (playerName.includes(inputValue)) {
        options[i].style.display = '';
      } else {
        options[i].style.display = 'none';
      }
    }
  });
});