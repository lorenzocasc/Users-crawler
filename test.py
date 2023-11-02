import openai


# Define your prompt

openai.api_key = "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"
model_engine = "gpt-3.5-turbo"


text =  "Ciao a tutti Da lunedì entrerà in vigore l'orario invernale per i musei civici: http://www.comune.genova.it/node/53367 Apertura mensile di Palazzo Lomellino http://www.genovapost.com/Genova/Cultura-e-Spettacolo/Palazzo-Lomellino-sabato-apertura-96046.aspx Apertura serale Palazzo Reale http://www.genovapost.com/Genova/Cultura-e-Spettacolo/Palazzo-Lomellino-sabato-apertura-96046.aspx Premiata a wiki loves monuments una foto scattata a Castello d'Albertis: http://www.museidigenova.it/it/content/castello-dalbertis-e-wiki-loves-monuments-2015 Giovedì 3 dicembre visita guidata per la Giornata internazionale dei diritti delle persone con disabilità http://www.genovapost.com/Genova/Cultura-e-Spettacolo/Palazzo-Reale-giovedi-visita-guidata-97197.aspx Prossimi eventi nei musei http://www.genovapost.com/Genova/Cultura-e-Spettacolo/Inaugura-venerdi-alle-ore-18-al-Museo-97255.aspx http://www.genovapost.com/Genova/Cultura-e-Spettacolo/Sabato-Insieme-al-Castello-aspettando-97258.aspx Per cortesia, sapete darmi notizie sugli orari del palazzo ducale per la mostra d'arte con le opere di Picasso, kandinsky, etc..??? Grazie mille!! ciao la mostra si chiama Dagli impressionisti a Picasso sul forum Genova c'è un post dedicato dove trovi tutte le informazioni e qualche commento di chi l'ha già vista ciao Grazie mille!!molto gentile!!buona serata!! figurati! Se quando hai visitato la mostra ti va di scrivere le tue impressioni sarà sicuramente un contributo utile Per gli altri utenti. Ciao Venerdi inaugurazione della mostra Ursus al Museo di Storia Naturale http://www.genovapost.com/Genova/Cultura-e-Spettacolo/Mostra-Ursus-da-venerdi-11-al-Museo-di-97518.aspx A Palazzo Rosso quattordici nuove opere restaurate: http://www.genovapost.com/Genova/Cultura-e-Spettacolo/Palazzo-Rosso-visibili-al-pubblico-97561.aspx "
# Make an API call to generate text
response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "You are a helpful assistant, expert of Project Design."},
        {"role": "user", "content": "Based on the text provided next, list users and needs" },
    ])

message = response.choices[0]['message']
print("{}: {}".format(message['role'], message['content']))
