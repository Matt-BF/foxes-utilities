import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import argparse
import warnings
import os

warnings.filterwarnings(action="ignore")


def auto_laudo(result_table, validate=True):
    INCONCLUSIVE = []
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}

    driver = webdriver.Chrome(
        executable_path=ChromeDriverManager().install(), options=options
    )

    driver.get("https://app.worklabweb.com.br/index.php")

    # estou na tela de login
    user_box = driver.find_element_by_xpath(
        "/html/body/div/div/div[2]/div[1]/form/div[3]/div[1]/input"
    )  # user
    pass_box = driver.find_element_by_xpath(
        "/html/body/div/div/div[2]/div[1]/form/div[3]/div[2]/input"
    )  # pass
    submit = driver.find_element_by_xpath(
        "/html/body/div/div/div[2]/div[1]/form/div[5]/button"
    )

    user_box.send_keys("875mateus")
    pass_box.send_keys("Vq6Jq3wnk3GeCid")
    submit.click()

    # estou na tela home
    driver.find_element_by_xpath(
        "/html/body/form/div/div[1]/div[3]/div[2]/div/a[1]/img"
    ).click()  # tela de insercao de resultados

    print("\n", "INSERINDO LAUDOS", "\n")
    # estou na tela de insercao de resultados
    for code in result_table.index:
        if result_table.loc[code, "Result"] != "INCONCLUSIVO" and code.isdigit():
            # abrir pagina do paciente pelo codigo
            codigo = driver.find_element_by_id("tbCodigoPaciente")  # celula de codigo
            # apagar o que tiver na celula e escrever o codigo
            codigo.send_keys(Keys.CONTROL + "a")
            codigo.send_keys(Keys.DELETE)
            codigo.send_keys(code)
            codigo.send_keys(Keys.ENTER)

            # hora de laudar
            driver.find_element_by_id("btExame1").click()  # botao do exame
            try:
                resultado = driver.find_element_by_id("tbResultado4492")
            except Exception:
                resultado = driver.find_element_by_id("tbResultado4496")
            resultado.send_keys(Keys.CONTROL + "a")
            resultado.send_keys(Keys.DELETE)
            if result_table.loc[code, "Result"] == "POSITIVO":
                resultado.send_keys("P")
                driver.find_element_by_id("btSalvar").click()
            else:
                resultado.send_keys("N")
                driver.find_element_by_id("btSalvar").click()

        # salvar os inconclusivos para ver na mao
        else:
            INCONCLUSIVE.append(code)

    if validate:
        print("\n", "CONFERINDO RESULTADOS", "\n")
        driver.find_element_by_xpath("/html/body/div/div/div[1]/a/img").click()
        driver.find_element_by_xpath(
            "/html/body/form/div/div[1]/div[3]/div[2]/div/a[2]"
        ).click()

        for code in result_table.index:
            if result_table.loc[code, "Result"] != "INCONCLUSIVO" and code.isdigit():
                # abrir pagina do paciente pelo codigo
                codigo = driver.find_element_by_id(
                    "tbCodigoPaciente"
                )  # celula de codigo
                # apagar o que tiver na celula e escrever o codigo
                codigo.send_keys(Keys.CONTROL + "a")
                codigo.send_keys(Keys.DELETE)
                codigo.send_keys(code)
                codigo.send_keys(Keys.ENTER)

                driver.find_element_by_id("btExame1").click()
                time.sleep(0.5)  # para tentar burlar o delay ridiculo do worklab
                driver.find_element_by_id("btSalvar").click()

    driver.quit()

    print(INCONCLUSIVE, len(INCONCLUSIVE) - 2)
