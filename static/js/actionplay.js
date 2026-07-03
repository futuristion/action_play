ActionPlay = {

    attemptId: null,

    playerName: "",

    start(data){

        this.attemptId = data.attempt_id;

        this.playerName = data.player_name;

    },

    finish(score){

        fetch("/api/e/cafe-terra-brasil/save-score/",{

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify({

                attempt_id:this.attemptId,

                score:score

            })

        });

    }

}