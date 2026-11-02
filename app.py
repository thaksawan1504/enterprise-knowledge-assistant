import os
import sys

from dotenv import load_dotenv

from rag import RAGBrain
from orchestrator import QueryOrchestrator
from sql_tool import SQLTool

load_dotenv()


def main():

    print("\n=== Enterprise Knowledge Assistant ===")

    data_dir = os.path.join(
        os.path.dirname(__file__),
        "data",
        "pdfs"
    )

    pdf_files = [
        f
        for f in os.listdir(data_dir)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:

        print(
            f"\n[!] Error: No PDF file found in '{data_dir}/' folder."
        )

        sys.exit(0)

    selected_pdf_name = pdf_files[0]

    selected_pdf_path = os.path.join(
        data_dir,
        selected_pdf_name
    )

    print(
        f"\n[Loading Document]: {selected_pdf_name}"
    )

    brain = RAGBrain()

    orchestrator = QueryOrchestrator()

    sql_tool = SQLTool()

    try:

        chunks_count = brain.process_document(
            selected_pdf_path
        )

        print(
            f"\n[Success] PDF processed into {chunks_count} chunks."
        )

    except Exception as e:

        print(
            f"\n[Initialization Failed] {str(e)}"
        )

        sys.exit(1)

    print(
        "\nSystem ready! Type your question below."
    )

    while True:

        try:

            user_q = input(
                "\nYour Question >> "
            )

            if user_q.lower() in [
                "exit",
                "quit"
            ]:

                print(
                    "\nGoodbye!"
                )

                break

            route = orchestrator.route_query(
                user_q
            )

            print(
                f"\n[Orchestrator Route]: {route}"
            )

            if route == "sql":

                response = sql_tool.get_employees()

            else:

                response = brain.execute_query(
                    user_q
                )

            print(
                f"\nAI Answer >> {response}"
            )

        except KeyboardInterrupt:

            print(
                "\nGoodbye!"
            )

            break

        except Exception as e:

            print(
                f"\nError: {str(e)}"
            )


if __name__ == "__main__":
    main()