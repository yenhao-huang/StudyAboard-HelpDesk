import ChatbotUI from "./MultiTurnChat";
import { sseProvider } from "./providers"; // 或 simpleProvider
export default function App() {
  return <ChatbotUI chatProvider={sseProvider} />;
}
