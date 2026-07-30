const ActionPlay = {
    attemptId: null,
    playerName: "",
    eventSlug: "",

    start(data) {
        if (!data || !data.attempt_id || !data.event_slug) {
            console.error(
                "Action Play: dados inválidos para iniciar a partida.",
                data
            );

            return false;
        }

        this.attemptId = data.attempt_id;
        this.playerName = data.player_name || "";
        this.eventSlug = data.event_slug;

        return true;
    },

    async finish(score) {
        if (!this.attemptId || !this.eventSlug) {
            console.error(
                "Action Play: tentativa ou evento não inicializado."
            );

            return {
                ok: false,
                error: "Partida não inicializada.",
            };
        }

        const numericScore = Number(score);

        if (!Number.isFinite(numericScore) || numericScore < 0) {
            console.error(
                "Action Play: pontuação inválida.",
                score
            );

            return {
                ok: false,
                error: "Pontuação inválida.",
            };
        }

        try {
            const response = await fetch(
                `/api/e/${encodeURIComponent(this.eventSlug)}/save-score/`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        attempt_id: this.attemptId,
                        score: Math.floor(numericScore),
                    }),
                }
            );

            const data = await response.json();

            if (!response.ok || !data.ok) {
                throw new Error(
                    data.error || "Não foi possível salvar a pontuação."
                );
            }

            return data;
        } catch (error) {
            console.error(
                "Action Play: erro ao salvar pontuação.",
                error
            );

            return {
                ok: false,
                error: error.message,
            };
        }
    },
};