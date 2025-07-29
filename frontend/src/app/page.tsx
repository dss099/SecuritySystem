import { redirect } from "next/navigation";

export default function HomePage() {
  // 默认重定向到“经营总览”页面
  redirect("/overview");
}
