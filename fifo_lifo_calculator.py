import pandas as pd

def calculate_fifo_lifo(transactions):
    # Spalten für FIFO- und LIFO-Gewinne hinzufügen
    transactions['FIFO_Gewinn'] = 0.0
    transactions['LIFO_Gewinn'] = 0.0
    
    # Listen für Käufe
    fifo_purchases = []
    lifo_purchases = []

    # Iteriere über die Transaktionen
    for index, row in transactions.iterrows():
        if row['Aktion'] == 'Kauf':
            # Füge Käufe den FIFO- und LIFO-Listen hinzu
            fifo_purchases.append([row['Menge'], row['Preis pro Aktie']])
            lifo_purchases.insert(0, [row['Menge'], row['Preis pro Aktie']])  # Für LIFO immer vorne einfügen

        elif row['Aktion'] == 'Verkauf':
            # Berechnung für FIFO
            sell_qty = row['Menge']
            fifo_total_cost = 0.0
            fifo_purchases_to_remove = []
            for purchase in fifo_purchases:
                if sell_qty <= 0:
                    break
                if purchase[0] >= sell_qty:
                    fifo_total_cost += sell_qty * purchase[1]
                    purchase[0] -= sell_qty
                    if purchase[0] == 0:
                        fifo_purchases_to_remove.append(purchase)
                    sell_qty = 0
                else:
                    fifo_total_cost += purchase[0] * purchase[1]
                    sell_qty -= purchase[0]
                    fifo_purchases_to_remove.append(purchase)
            for p in fifo_purchases_to_remove:
                fifo_purchases.remove(p)
            fifo_profit = (row['Preis pro Aktie'] * abs(row['Menge'])) - fifo_total_cost
            transactions.at[index, 'FIFO_Gewinn'] = fifo_profit

            # Berechnung für LIFO
            sell_qty = row['Menge']
            lifo_total_cost = 0.0
            lifo_purchases_to_remove = []
            for purchase in lifo_purchases:
                if sell_qty <= 0:
                    break
                if purchase[0] >= sell_qty:
                    lifo_total_cost += sell_qty * purchase[1]
                    purchase[0] -= sell_qty
                    if purchase[0] == 0:
                        lifo_purchases_to_remove.append(purchase)
                    sell_qty = 0
                else:
                    lifo_total_cost += purchase[0] * purchase[1]
                    sell_qty -= purchase[0]
                    lifo_purchases_to_remove.append(purchase)
            for p in lifo_purchases_to_remove:
                lifo_purchases.remove(p)
            lifo_profit = (row['Preis pro Aktie'] * abs(row['Menge'])) - lifo_total_cost
            transactions.at[index, 'LIFO_Gewinn'] = lifo_profit

    return transactions

# CSV/Excel importieren und exportieren
def process_transactions(input_file, output_file):
    # Datei laden (CSV oder Excel)
    if input_file.endswith('.csv'):
        transactions = pd.read_csv(input_file)
    elif input_file.endswith('.xlsx'):
        transactions = pd.read_excel(input_file)

    # Berechne FIFO und LIFO
    transactions_with_profit = calculate_fifo_lifo(transactions)

    # Datei als Excel exportieren
    transactions_with_profit.to_excel(output_file, index=False)
    print(f'Die berechneten Transaktionen wurden in {output_file} gespeichert.')

if __name__ == "__main__":
    # Datei einlesen und Ergebnis exportieren
    input_file = 'transaktionen.xlsx'  # Beispiel: Eingabedatei
    output_file = 'transaktionen_berechnet.xlsx'  # Beispiel: Ausgabedatei

    process_transactions(input_file, output_file)
