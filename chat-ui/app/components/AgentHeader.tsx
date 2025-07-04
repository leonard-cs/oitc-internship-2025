export default function AgentHeader() {
  return (
    <header className="bg-white p-4">
      <div className="flex lg:flex-1 items-center justify-center">
        {/* <a href="#" className="m-1.5">
          <span className="sr-only">Text-to-SQL Agent</span>
          <img
            className="h-8 w-auto"
            src="http://localhost:3000/watsonx.svg"
            alt=""
          />
        </a> */}
        <h1 className="text-black font-bold">Database Query Agent</h1>
      </div>
    </header>
  )
}
