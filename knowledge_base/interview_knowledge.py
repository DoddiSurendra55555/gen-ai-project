
"""
General interview knowledge for the Hybrid RAG system.

This knowledge base contains reusable interview concepts.
Candidate-specific information comes separately from the
uploaded resume.
"""


INTERVIEW_KNOWLEDGE = [

    # -----------------------------------------------------
    # PROGRAMMING FUNDAMENTALS
    # -----------------------------------------------------

    {
        "topic": "Programming Fundamentals",
        "text": """
        Programming fundamentals include variables, data types,
        operators, conditional statements, loops, functions,
        recursion, and error handling.

        Variables store information. Data types define the kind
        of information stored, such as integers, strings,
        floating-point numbers, and Boolean values.

        Conditional statements allow programs to make decisions.
        Loops execute instructions repeatedly. Functions organize
        reusable logic and improve code maintainability.

        Recursion occurs when a function calls itself. It requires
        a base condition to prevent infinite recursion.

        Exception handling allows applications to respond to
        unexpected errors without terminating unnecessarily.

        Interviewers may ask candidates to explain programming
        concepts, solve logical problems, compare approaches,
        and describe how they debug code.
        """
    },

    # -----------------------------------------------------
    # DATA STRUCTURES AND ALGORITHMS
    # -----------------------------------------------------

    {
        "topic": "Data Structures and Algorithms",
        "text": """
        Data structures organize information for efficient
        storage and retrieval.

        Arrays store elements in indexed positions. Linked lists
        connect elements through references. Stacks follow
        Last In First Out behavior. Queues follow First In
        First Out behavior.

        Hash tables store key-value pairs and commonly provide
        average constant-time lookup.

        Trees represent hierarchical information. Binary search
        trees organize values according to ordering rules.
        Graphs represent relationships between connected nodes.

        Sorting algorithms arrange data. Searching algorithms
        locate specific elements.

        Big O notation describes how algorithm performance
        changes as input size increases.

        Common complexities include O(1), O(log n), O(n),
        O(n log n), and O(n squared).

        Interviewers evaluate problem-solving ability, correctness,
        time complexity, space complexity, and code clarity.
        """
    },

    # -----------------------------------------------------
    # PYTHON
    # -----------------------------------------------------

    {
        "topic": "Python Programming",
        "text": """
        Python is a high-level programming language known for
        readable syntax and a large ecosystem of libraries.

        Important concepts include lists, tuples, dictionaries,
        sets, functions, classes, modules, decorators,
        generators, comprehensions, and exception handling.

        Lists are mutable sequences. Tuples are immutable
        sequences. Dictionaries store key-value mappings.
        Sets store unique elements.

        Object-oriented programming in Python uses classes
        and objects. Important principles include encapsulation,
        inheritance, abstraction, and polymorphism.

        Generators produce values lazily and can reduce memory
        usage when processing large sequences.

        Python interview questions may involve coding,
        debugging, data manipulation, object-oriented design,
        and performance considerations.
        """
    },

    # -----------------------------------------------------
    # DATABASES AND SQL
    # -----------------------------------------------------

    {
        "topic": "Databases and SQL",
        "text": """
        A database stores and organizes information.

        Relational databases organize information into tables
        containing rows and columns. SQL is used to create,
        retrieve, update, and delete relational data.

        Important SQL operations include SELECT, INSERT,
        UPDATE, DELETE, JOIN, GROUP BY, ORDER BY, and HAVING.

        Primary keys uniquely identify records. Foreign keys
        establish relationships between tables.

        Database normalization reduces unnecessary duplication
        and helps maintain data consistency.

        Indexes can improve query performance but require
        additional storage and may slow down write operations.

        Transactions follow ACID principles:
        Atomicity, Consistency, Isolation, and Durability.

        Interviewers may ask candidates to write SQL queries,
        explain joins, design schemas, and optimize queries.
        """
    },

    # -----------------------------------------------------
    # MACHINE LEARNING AND AI
    # -----------------------------------------------------

    {
        "topic": "Machine Learning and Artificial Intelligence",
        "text": """
        Artificial intelligence involves building systems
        capable of performing tasks that typically require
        human intelligence.

        Machine learning allows systems to learn patterns
        from data.

        Supervised learning uses labeled training data.
        Unsupervised learning identifies patterns in
        unlabeled data. Reinforcement learning learns
        through actions, rewards, and feedback.

        Classification predicts categories. Regression
        predicts numerical values. Clustering groups
        similar data points.

        Training data is used to fit a model. Validation
        data helps tune model parameters. Test data measures
        performance on unseen examples.

        Overfitting occurs when a model performs well on
        training data but poorly on new data. Underfitting
        occurs when a model fails to learn important patterns.

        Common evaluation metrics include accuracy, precision,
        recall, F1-score, mean absolute error, and mean
        squared error.

        Interviewers may ask about algorithms, feature
        engineering, model evaluation, data preparation,
        and real-world applications.
        """
    },

    # -----------------------------------------------------
    # DEEP LEARNING AND GENERATIVE AI
    # -----------------------------------------------------

    {
        "topic": "Deep Learning and Generative AI",
        "text": """
        Deep learning uses neural networks with multiple
        processing layers to learn complex patterns.

        Neural networks contain interconnected artificial
        neurons. Activation functions introduce non-linearity.

        Common architectures include convolutional neural
        networks, recurrent neural networks, and transformers.

        Transformers use attention mechanisms to process
        relationships between elements in input sequences.

        Generative AI creates new content such as text,
        images, audio, and code.

        Large language models generate text based on patterns
        learned during training.

        Prompt engineering involves writing clear instructions
        and providing useful context to guide model responses.

        Retrieval-Augmented Generation, or RAG, combines
        information retrieval with generative AI.

        A RAG system retrieves relevant information from
        external documents and provides that information
        as context to a language model.

        Embeddings represent text as numerical vectors.
        Semantic similarity helps retrieve information
        with related meanings.

        RAG systems can improve grounding, but retrieved
        information must still be checked for relevance,
        accuracy, and completeness.
        """
    },

    # -----------------------------------------------------
    # WEB DEVELOPMENT
    # -----------------------------------------------------

    {
        "topic": "Web Development",
        "text": """
        Web development involves building applications
        that operate through web browsers and servers.

        HTML defines webpage structure. CSS controls
        presentation. JavaScript adds interactive behavior.

        Frontend development focuses on the user interface.
        Backend development handles application logic,
        data processing, and server-side operations.

        APIs allow different software systems to communicate.

        REST APIs commonly use HTTP methods such as GET,
        POST, PUT, PATCH, and DELETE.

        HTTP status codes communicate request outcomes.
        For example, 200 indicates success, 404 indicates
        a missing resource, and 500 indicates a server error.

        Authentication verifies identity. Authorization
        determines what an authenticated user can access.

        Interviewers may ask about API design, HTTP methods,
        client-server communication, and application security.
        """
    },

    # -----------------------------------------------------
    # CLOUD COMPUTING AND DEPLOYMENT
    # -----------------------------------------------------

    {
        "topic": "Cloud Computing and Deployment",
        "text": """
        Cloud computing provides computing resources such
        as servers, storage, databases, and networking
        through internet-based services.

        Infrastructure as a Service provides virtualized
        infrastructure. Platform as a Service provides
        an environment for deploying applications.
        Software as a Service provides ready-to-use
        software applications.

        Deployment makes an application available to users.

        Environment variables and secret management help
        protect credentials and configuration values.

        Continuous Integration involves automatically
        checking code changes. Continuous Deployment
        automates releasing tested application changes.

        Logging and monitoring help identify application
        errors and performance problems.

        Interviewers may ask about deployment workflows,
        scalability, configuration, cloud services,
        and production troubleshooting.
        """
    },

    # -----------------------------------------------------
    # SOFTWARE ENGINEERING
    # -----------------------------------------------------

    {
        "topic": "Software Engineering",
        "text": """
        Software engineering applies systematic methods
        to designing, developing, testing, and maintaining
        software systems.

        Important principles include modularity,
        maintainability, reusability, readability,
        separation of concerns, and low coupling.

        Object-oriented programming organizes software
        around objects and classes.

        Design patterns provide reusable approaches
        to recurring software design problems.

        Version control systems track code changes.
        Git supports branching, merging, commits,
        and collaboration.

        Agile development emphasizes iterative work,
        collaboration, feedback, and continuous improvement.

        Interviewers may ask candidates to explain
        architecture decisions, teamwork, code quality,
        and development workflows.
        """
    },

    # -----------------------------------------------------
    # TESTING AND DEBUGGING
    # -----------------------------------------------------

    {
        "topic": "Software Testing and Debugging",
        "text": """
        Software testing checks whether an application
        behaves as expected.

        Unit testing checks individual functions or
        components. Integration testing checks whether
        multiple components work together.

        System testing evaluates the complete application.
        Acceptance testing checks whether the application
        satisfies user requirements.

        Regression testing ensures new changes do not
        break existing functionality.

        Debugging identifies and fixes errors.

        Useful debugging techniques include reading
        error messages, reproducing problems, inspecting
        variable values, adding logs, and isolating
        the failing component.

        Good tests cover normal inputs, boundary conditions,
        invalid inputs, and unexpected situations.
        """
    },

    # -----------------------------------------------------
    # CYBERSECURITY
    # -----------------------------------------------------

    {
        "topic": "Cybersecurity Fundamentals",
        "text": """
        Cybersecurity protects systems, applications,
        networks, and information from unauthorized access
        and malicious activity.

        The CIA triad consists of confidentiality,
        integrity, and availability.

        Authentication verifies a user's identity.
        Authorization controls permitted actions.

        Encryption protects information by converting
        readable data into an encoded form.

        Passwords should be stored using secure password
        hashing rather than plain text.

        Common security concerns include injection attacks,
        cross-site scripting, broken access controls,
        insecure configuration, and exposed credentials.

        Interviewers may ask about secure coding,
        access management, data protection, and
        application vulnerabilities.
        """
    },

    # -----------------------------------------------------
    # PROJECT EXPLANATION
    # -----------------------------------------------------

    {
        "topic": "Project Explanation",
        "text": """
        Candidates should be able to explain their projects
        clearly and accurately.

        A strong project explanation includes:

        1. Problem statement: What problem did the project solve?
        2. Objective: What was the intended outcome?
        3. Technology: Which tools and technologies were used?
        4. Architecture: How were the components connected?
        5. Contribution: What work did the candidate personally do?
        6. Challenges: What technical difficulties occurred?
        7. Solution: How were those difficulties addressed?
        8. Results: What was achieved?
        9. Improvements: What could be enhanced in the future?

        Interviewers may ask candidates to explain technical
        decisions, demonstrate their contribution, discuss
        limitations, and suggest improvements.

        Candidates should not claim responsibilities or
        results they cannot support with genuine examples.
        """
    },

    # -----------------------------------------------------
    # BEHAVIORAL INTERVIEW
    # -----------------------------------------------------

    {
        "topic": "Behavioral Interview and STAR Method",
        "text": """
        Behavioral interviews evaluate how candidates
        handled situations in their previous experiences.

        The STAR method organizes answers into four parts:

        Situation: Explain the background and context.
        Task: Describe the responsibility or objective.
        Action: Explain the specific steps personally taken.
        Result: Describe the outcome and lessons learned.

        Common behavioral topics include teamwork,
        leadership, conflict resolution, problem-solving,
        adaptability, communication, and time management.

        Strong answers use specific examples rather than
        vague statements.

        Candidates should explain their personal contribution
        clearly, acknowledge challenges, and describe
        what they learned from the experience.
        """
    },

    # -----------------------------------------------------
    # HR AND COMMUNICATION
    # -----------------------------------------------------

    {
        "topic": "HR Interview and Communication",
        "text": """
        HR interviews often evaluate communication,
        motivation, professional goals, adaptability,
        and understanding of a role.

        Common questions include:

        Tell me about yourself.
        Why are you interested in this role?
        What are your strengths?
        What skills are you improving?
        Why should we hire you?
        Where do you see yourself in five years?
        Describe a challenge you overcame.

        Effective answers should be honest, relevant,
        structured, and supported by examples.

        Candidates should connect their skills and
        experiences to the requirements of the role.

        When discussing weaknesses, candidates should
        explain genuine areas for improvement and
        the steps they are taking to develop.
        """
    },

    # -----------------------------------------------------
    # COMMUNICATION AND PROBLEM SOLVING
    # -----------------------------------------------------

    {
        "topic": "Problem Solving and Communication",
        "text": """
        Technical interviewers evaluate not only the
        final answer but also the candidate's reasoning.

        A structured problem-solving approach includes:

        1. Understand the problem.
        2. Identify assumptions and constraints.
        3. Break the problem into smaller parts.
        4. Consider possible approaches.
        5. Compare trade-offs.
        6. Explain the selected solution.
        7. Test the solution with examples.
        8. Discuss complexity and possible improvements.

        Candidates should ask clarifying questions when
        requirements are unclear.

        Clear communication, logical reasoning, and the
        ability to explain decisions are important
        interview skills.
        """
    },

]


def get_general_knowledge_documents():
    """
    Return general interview knowledge in the document
    format expected by utils.rag_engine.

    Each topic becomes an independent document.
    """

    documents = []

    for item in INTERVIEW_KNOWLEDGE:

        documents.append({
            "text": (
                f"Topic: {item['topic']}\n\n"
                f"{item['text'].strip()}"
            ),
            "source": "general",
            "topic": item["topic"],
        })

    return documents


def get_available_topics():
    """Return the list of available knowledge topics."""

    return [
        item["topic"]
        for item in INTERVIEW_KNOWLEDGE
    ]
