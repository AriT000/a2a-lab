from client.client import A2AClient

def main():
    with A2AClient("https://echo-a2a-agent-741297514794.us-central1.run.app") as client:
        card = client.fetch_agent_card()

        agent_name = card.get("name", "<unknown>")
        skills = client.get_skills()

        print(f"Agent name: {agent_name}")
        print("Skills:")
        if skills:
            for skill in skills:
                if isinstance(skill, dict):
                    print(f"  - {skill.get('name', skill)}")
                else:
                    print(f"  - {skill}")
        else:
            print("  (none)")

        response = client.send_task("Hello from the client!")
        echoed = client.extract_text(response)

        print("\nResponse:")
        print(echoed)

if __name__ == "__main__":
    main()
