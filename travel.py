import uuid
import copy
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

#usado bibliotecas padrão do python

# simulando um "banco de dados" em memória)
itineraries_data = []
current_itinerary_id = None

#  Itinerários (Menu de Sugestões) 
# Esta lista serve como um catálogo de opções prontas para o usuário
predefined_itineraries = [
    {
        "title": "Férias na Itália: Roma e Florença",
        "start_date": "2024-09-01",
        "end_date": "2024-09-10",
        "activities": [
            {"id": str(uuid.uuid4()), "name": "Visita ao Coliseu", "type": "passeio", "date": "2024-09-02", "time": "10:00", "description": "Explorar a história do Império Romano."},
            {"id": str(uuid.uuid4()), "name": "Degustação de Vinhos na Toscana", "type": "passeio", "date": "2024-09-06", "time": "14:00", "description": "Tour por vinícolas e degustação de vinhos locais."}
        ],
        "expenses": [
            {"id": str(uuid.uuid4()), "description": "Passagem de avião", "amount": 2500.00, "date": "2024-07-20"}
        ]
    },
    {
        "title": "Aventura na Amazônia",
        "start_date": "2024-11-15",
        "end_date": "2024-11-22",
        "activities": [
            {"id": str(uuid.uuid4()), "name": "Trilha pela floresta", "type": "aventura", "date": "2024-11-16", "time": "08:00", "description": "Caminhada guiada para observação de fauna e flora."},
            {"id": str(uuid.uuid4()), "name": "Passeio de barco pelo Rio Negro", "type": "passeio", "date": "2024-11-18", "time": "15:30", "description": "Contemplar o pôr do sol no rio."}
        ],
        "expenses": [
            {"id": str(uuid.uuid4()), "description": "Hospedagem em ecopousada", "amount": 1200.00, "date": "2024-07-25"}
        ]
    }
]

#  Funções Utilitárias 

def generate_unique_id():
    """Gera um ID único usando UUID."""
    return str(uuid.uuid4())

def format_currency(amount):
    """Formata um valor numérico como moeda brasileira."""
    return f"R$ {amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

#  (Lógica do Programa) 

def create_itinerary(title, start_date_str, end_date_str):
    """Cria um novo itinerário e o adiciona à lista global."""
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        messagebox.showerror("Erro de Data", "Formato de data inválido. Use YYYY-MM-DD.")
        return None

    if start_date > end_date:
        messagebox.showerror("Erro de Data", "A data de início não pode ser posterior à data de término.")
        return None

    new_itinerary = {
        "id": generate_unique_id(),
        "title": title,
        "start_date": start_date_str,
        "end_date": end_date_str,
        "activities": [],
        "expenses": []
    }
    itineraries_data.append(new_itinerary)
    messagebox.showinfo("Sucesso", f"Itinerário '{title}' criado com sucesso!")
    return new_itinerary

def add_activity_to_itinerary(itinerary_id, name, activity_type, date_str, time_str, description):
    """Adiciona uma atividade a um itinerário específico."""
    itinerary = find_itinerary_by_id(itinerary_id)
    if not itinerary:
        messagebox.showerror("Erro", "Itinerário não encontrado.")
        return None

    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        datetime.strptime(time_str, '%H:%M')
    except ValueError:
        messagebox.showerror("Erro de Formato", "Formato de data (YYYY-MM-DD) ou hora (HH:MM) inválido.")
        return None

    new_activity = {
        "id": generate_unique_id(),
        "name": name,
        "type": activity_type,
        "date": date_str,
        "time": time_str,
        "description": description
    }
    itinerary["activities"].append(new_activity)
    messagebox.showinfo("Sucesso", f"Atividade '{name}' adicionada.")
    return new_activity

def add_expense_to_itinerary(itinerary_id, description, amount):
    """Adiciona uma despesa a um itinerário específico."""
    itinerary = find_itinerary_by_id(itinerary_id)
    if not itinerary:
        messagebox.showerror("Erro", "Itinerário não encontrado.")
        return None

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("O valor da despesa deve ser positivo.")
    except ValueError as e:
        messagebox.showerror("Erro", f"Valor da despesa inválido. {e}")
        return None

    new_expense = {
        "id": generate_unique_id(),
        "description": description,
        "amount": amount,
        "date": datetime.now().strftime('%Y-%m-%d')
    }
    itinerary["expenses"].append(new_expense)
    messagebox.showinfo("Sucesso", f"Despesa '{description}' adicionada.")
    return new_expense

def find_itinerary_by_id(itinerary_id):
    """Encontra um itinerário pelo seu ID."""
    for itinerary in itineraries_data:
        if itinerary["id"] == itinerary_id:
            return itinerary
    return None

# --- Funções da Interface Gráfica (GUI) ---

def show_main_menu():
    """Exibe o menu principal com a lista de itinerários."""
    for widget in main_frame.winfo_children():
        widget.destroy()
    details_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

    title_label = ttk.Label(main_frame, text="Travel Itinerary Planner", font=("Helvetica", 20, "bold"))
    title_label.pack(pady=10)

    # --- Seção de Criação de Itinerário ---
    create_frame = ttk.LabelFrame(main_frame, text="Criar Novo Itinerário", padding=10)
    create_frame.pack(pady=10, padx=10, fill="x")

    create_frame.columnconfigure(1, weight=1)

    ttk.Label(create_frame, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    title_entry = ttk.Entry(create_frame)
    title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(create_frame, text="Data Início (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    start_date_entry = ttk.Entry(create_frame)
    start_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(create_frame, text="Data Fim (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    end_date_entry = ttk.Entry(create_frame)
    end_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    create_button = ttk.Button(create_frame, text="Criar Itinerário",
                               command=lambda: handle_create_itinerary(title_entry, start_date_entry, end_date_entry, itinerary_listbox))
    create_button.grid(row=3, column=0, columnspan=2, pady=10)

    # --- Seção de Visualização de Itinerários Sugeridos ---
    suggested_frame = ttk.LabelFrame(main_frame, text="Itinerários Sugeridos", padding=10)
    suggested_frame.pack(pady=10, padx=10, fill="x")

    suggested_listbox = tk.Listbox(suggested_frame, height=5, bg='#e0f7fa', fg='#01579b', selectbackground='#0277bd', selectforeground='white')
    for itinerary in predefined_itineraries:
        suggested_listbox.insert(tk.END, itinerary["title"])
    suggested_listbox.pack(pady=5, fill="x", expand=True)

    add_suggested_button = ttk.Button(suggested_frame, text="Adicionar Itinerário Sugerido",
                                      command=lambda: handle_add_predefined_itinerary(suggested_listbox, itinerary_listbox))
    add_suggested_button.pack(pady=5)

    # --- Seção de Visualização de Meus Itinerários ---
    itineraries_frame = ttk.LabelFrame(main_frame, text="Meus Itinerários", padding=10)
    itineraries_frame.pack(pady=10, padx=10, fill="x", expand=True)

    itinerary_listbox = tk.Listbox(itineraries_frame, height=10, bg='#ffffff', fg='#333333', selectbackground='#00796b', selectforeground='white')
    itinerary_listbox.pack(fill="both", expand=True)
    itinerary_listbox.bind("<<ListboxSelect>>", lambda event: handle_itinerary_selection(itinerary_listbox))

    refresh_itinerary_list(itinerary_listbox)

def refresh_itinerary_list(listbox):
    """Atualiza a Listbox com os itinerários da lista global."""
    listbox.delete(0, tk.END)
    if not itineraries_data:
        listbox.insert(tk.END, "Nenhum itinerário criado ainda.")
    else:
        for itinerary in itineraries_data:
            listbox.insert(tk.END, f"{itinerary['title']} ({itinerary['start_date']} a {itinerary['end_date']})")

def handle_create_itinerary(title_entry, start_date_entry, end_date_entry, listbox):
    """Função de callback para o botão 'Criar Itinerário'."""
    title = title_entry.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    if title and start_date and end_date:
        create_itinerary(title, start_date, end_date)
        refresh_itinerary_list(listbox)
        title_entry.delete(0, tk.END)
        start_date_entry.delete(0, tk.END)
        end_date_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos para criar um itinerário.")

def handle_add_predefined_itinerary(suggested_listbox, my_itineraries_listbox):
    """Função para adicionar um itinerário sugerido à lista do usuário."""
    try:
        selected_index = suggested_listbox.curselection()[0]
        itinerary_to_add = copy.deepcopy(predefined_itineraries[selected_index])
        itinerary_to_add["id"] = generate_unique_id() # Garante um ID único
        
        itineraries_data.append(itinerary_to_add)
        messagebox.showinfo("Sucesso", f"Itinerário '{itinerary_to_add['title']}' adicionado com sucesso!")
        refresh_itinerary_list(my_itineraries_listbox)
    except IndexError:
        messagebox.showwarning("Nenhuma seleção", "Por favor, selecione um itinerário sugerido para adicionar.")
        pass

def handle_itinerary_selection(listbox):
    """Função de callback para quando um itinerário é selecionado na lista."""
    try:
        selected_index = listbox.curselection()[0]
        itinerary = itineraries_data[selected_index]
        show_itinerary_details(itinerary)
    except IndexError:
        pass

def show_itinerary_details(itinerary):
    """Exibe os detalhes de um itinerário específico."""
    global current_itinerary_id
    current_itinerary_id = itinerary["id"]
    main_frame.pack_forget()
    details_frame.pack(pady=10, padx=10, fill="both", expand=True)

    for widget in details_frame.winfo_children():
        widget.destroy()

    # --- Seção de Detalhes do Itinerário ---
    ttk.Label(details_frame, text=f"Detalhes do Itinerário: {itinerary['title']}", font=("Helvetica", 16, "bold")).pack(pady=5)
    ttk.Label(details_frame, text=f"Período: {itinerary['start_date']} a {itinerary['end_date']}").pack(pady=5)

    back_button = ttk.Button(details_frame, text="← Voltar para a lista", command=show_main_menu)
    back_button.pack(pady=5)

    # --- Notebook para Atividades e Despesas ---
    notebook = ttk.Notebook(details_frame)
    notebook.pack(pady=10, padx=10, fill="both", expand=True)

    activities_tab = ttk.Frame(notebook)
    expenses_tab = ttk.Frame(notebook)
    notebook.add(activities_tab, text="Atividades")
    notebook.add(expenses_tab, text="Despesas")

    # --- Conteúdo da Aba de Atividades ---
    activities_tab.columnconfigure(1, weight=1)
    ttk.Label(activities_tab, text="Adicionar Atividade", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
    
    ttk.Label(activities_tab, text="Nome:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    activity_name_entry = ttk.Entry(activities_tab)
    activity_name_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

    ttk.Label(activities_tab, text="Tipo:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
    activity_type_entry = ttk.Entry(activities_tab)
    activity_type_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

    ttk.Label(activities_tab, text="Data:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
    activity_date_entry = ttk.Entry(activities_tab)
    activity_date_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

    ttk.Label(activities_tab, text="Hora:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
    activity_time_entry = ttk.Entry(activities_tab)
    activity_time_entry.grid(row=4, column=1, padx=5, pady=2, sticky="ew")

    ttk.Label(activities_tab, text="Descrição:").grid(row=5, column=0, padx=5, pady=2, sticky="w")
    activity_desc_entry = ttk.Entry(activities_tab)
    activity_desc_entry.grid(row=5, column=1, padx=5, pady=2, sticky="ew")

    activities_listbox = tk.Listbox(activities_tab, height=10)
    add_activity_button = ttk.Button(activities_tab, text="Adicionar Atividade",
                                    command=lambda: handle_add_activity(activity_name_entry, activity_type_entry, activity_date_entry, activity_time_entry, activity_desc_entry, activities_listbox, expenses_listbox, total_expenses_label))
    add_activity_button.grid(row=6, column=0, columnspan=2, pady=5)
    
    ttk.Label(activities_tab, text="Lista de Atividades", font=("Helvetica", 12, "bold")).grid(row=7, column=0, columnspan=2, pady=5)
    activities_listbox.grid(row=8, column=0, columnspan=2, pady=5, padx=10, sticky="nsew")

    # --- Conteúdo da Aba de Despesas ---
    expenses_tab.columnconfigure(1, weight=1)
    ttk.Label(expenses_tab, text="Adicionar Despesa", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
    
    ttk.Label(expenses_tab, text="Descrição:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    expense_desc_entry = ttk.Entry(expenses_tab)
    expense_desc_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

    ttk.Label(expenses_tab, text="Valor (ex: 150.75):").grid(row=2, column=0, padx=5, pady=2, sticky="w")
    expense_amount_entry = ttk.Entry(expenses_tab)
    expense_amount_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

    expenses_listbox = tk.Listbox(expenses_tab, height=10)
    total_expenses_label = ttk.Label(expenses_tab, text="Total: R$ 0,00", font=("Helvetica", 12, "bold"))
    
    add_expense_button = ttk.Button(expenses_tab, text="Adicionar Despesa",
                                    command=lambda: handle_add_expense(expense_desc_entry, expense_amount_entry, activities_listbox, expenses_listbox, total_expenses_label))
    add_expense_button.grid(row=3, column=0, columnspan=2, pady=5)

    ttk.Label(expenses_tab, text="Lista de Despesas", font=("Helvetica", 12, "bold")).grid(row=4, column=0, columnspan=2, pady=5)
    expenses_listbox.grid(row=5, column=0, columnspan=2, pady=5, padx=10, sticky="nsew")
    
    total_expenses_label.grid(row=6, column=0, columnspan=2, pady=5)

    refresh_activities_and_expenses(activities_listbox, expenses_listbox, total_expenses_label)

def handle_add_activity(name_entry, type_entry, date_entry, time_entry, desc_entry, activities_listbox, expenses_listbox, total_expenses_label):
    """Função de callback para adicionar atividade."""
    if not current_itinerary_id: return
    name = name_entry.get()
    activity_type = type_entry.get()
    date_str = date_entry.get()
    time_str = time_entry.get()
    description = desc_entry.get()
    
    if name and activity_type and date_str and time_str:
        add_activity_to_itinerary(current_itinerary_id, name, activity_type, date_str, time_str, description)
        refresh_activities_and_expenses(activities_listbox, expenses_listbox, total_expenses_label)
        name_entry.delete(0, tk.END)
        type_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Campos Vazios", "Por favor, preencha os campos obrigatórios.")

def handle_add_expense(desc_entry, amount_entry, activities_listbox, expenses_listbox, total_expenses_label):
    """Função de callback para adicionar despesa."""
    if not current_itinerary_id: return
    description = desc_entry.get()
    amount = amount_entry.get()

    if description and amount:
        add_expense_to_itinerary(current_itinerary_id, description, amount)
        refresh_activities_and_expenses(activities_listbox, expenses_listbox, total_expenses_label)
        desc_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos.")

def refresh_activities_and_expenses(activities_listbox, expenses_listbox, total_expenses_label):
    """Atualiza as listas de atividades e despesas para o itinerário atual."""
    itinerary = find_itinerary_by_id(current_itinerary_id)
    if not itinerary: return

    activities_listbox.delete(0, tk.END)
    if not itinerary["activities"]:
        activities_listbox.insert(tk.END, "Nenhuma atividade adicionada.")
    else:
        sorted_activities = sorted(
            itinerary["activities"],
            key=lambda x: (datetime.strptime(x['date'], '%Y-%m-%d'), datetime.strptime(x['time'], '%H:%M'))
        )
        for activity in sorted_activities:
            activities_listbox.insert(tk.END, f"[{activity['type']}] {activity['name']} em {activity['date']} às {activity['time']}")

    expenses_listbox.delete(0, tk.END)
    total_expenses = 0
    if not itinerary["expenses"]:
        expenses_listbox.insert(tk.END, "Nenhuma despesa registrada.")
    else:
        for expense in itinerary["expenses"]:
            expenses_listbox.insert(tk.END, f"{expense['date']}: {expense['description']} - {format_currency(expense['amount'])}")
            total_expenses += expense['amount']
    
    total_expenses_label.config(text=f"Total: {format_currency(total_expenses)}")


# --- Configuração da Janela Principal ---
root = tk.Tk()
root.title("Travel Itinerary Planner")
root.geometry("600x800")
style = ttk.Style(root)
style.theme_use('clam')

# Definir um estilo personalizado para cores e bordas
style.configure('TFrame', background='#f0f2f5')
style.configure('TLabel', background='#f0f2f5', foreground='#333333')
style.configure('TLabelFrame', background='#ffffff', foreground='#333333', relief='flat', borderwidth=1)
style.configure('TLabelFrame.Label', background='#ffffff', font=('Helvetica', 12, 'bold'))
style.configure('TButton', background='#4a90e2', foreground='white', font=('Helvetica', 10, 'bold'))
style.map('TButton',
          background=[('active', '#3672b8')],
          foreground=[('active', 'white')])
style.configure('TEntry', fieldbackground='white', foreground='#333333')
style.configure('TNotebook', background='#f0f2f5')
style.configure('TNotebook.Tab', background='#cccccc', foreground='#555555')
style.map('TNotebook.Tab',
          background=[('selected', '#4a90e2')],
          foreground=[('selected', 'white')])


# Criar os dois frames principais, usando o estilo personalizado
main_frame = ttk.Frame(root, padding="10")
details_frame = ttk.Frame(root, padding="10")

# Iniciar o aplicativo com o menu principal
show_main_menu()

root.mainloop()
