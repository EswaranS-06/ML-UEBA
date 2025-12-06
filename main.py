from preprocess.preprocess_pipeline import PreprocessPipeline

def main():
    pipeline = PreprocessPipeline()

    # Example mixed-source logs
    logs = [
        "Jan 10 12:00:01 serverA sshd: User login failed",
        {
            "EventID": 4624,
            "ComputerName": "WIN-SERVER",
            "User": "Administrator",
            "IpAddress": "10.0.0.15",
            "ProcessName": "svchost.exe",
            "Message": "User Logon",
            "TimeCreated": "2025-01-20T10:20:00Z"
        },
        {
            "eventTime": "2025-01-20T08:22:33Z",
            "eventName": "ConsoleLogin",
            "userIdentity": {"userName": "ec2-user"},
            "sourceIPAddress": "54.120.21.3",
            "eventSource": "signin.amazonaws.com",
            "requestParameters": {"mfa": True}
        },
    ]

    df = pipeline.run(logs)
    print(df)

if __name__ == "__main__":
    main()
