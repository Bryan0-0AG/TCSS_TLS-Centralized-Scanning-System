from dashboard import crear_app

if __name__ == "__main__":
    print("\nAbriendo dashboard en el navegador...")
    print("Ve a: http://127.0.0.1:8050\n")
    app = crear_app()
    app.run(debug=False)
