class QueryOrchestrator:

    def route_query(self, query):

        q = query.lower()

        if any(
            word in q
            for word in [
                "employee",
                "employees",
                "salary",
                "department"
            ]
        ):
            return "sql"

        elif any(
            word in q
            for word in [
                "release",
                "version",
                "deployment"
            ]
        ):
            return "release"

        elif any(
            word in q
            for word in [
                "support",
                "issue",
                "error",
                "incident"
            ]
        ):
            return "support"

        elif any(
            word in q
            for word in [
                "exam",
                "date",
                "subject",
                "semester",
                "course",
                "schedule"
            ]
        ):
            return "academic"

        else:
            return "general"