import { useState } from 'react'
import { 
  Sparkles, 
  Phone, 
  Mail, 
  CreditCard, 
  Download, 
  Copy, 
  Check,
  Settings,
  Database,
  Wand2,
  ChevronRight,
  Github,
  AlertCircle
} from 'lucide-react'

const API_BASE = 'http://localhost:8000/api'

interface DataItem {
  phone?: string
  email?: string
  id_card?: string
}

interface GenerateResponse {
  success: boolean
  count: number
  data: DataItem[]
}

function App() {
  const [count, setCount] = useState(10)
  const [data, setData] = useState<DataItem[]>([])
  const [copied, setCopied] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async () => {
    setIsGenerating(true)
    setError(null)
    
    try {
      const response = await fetch(`${API_BASE}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          count,
          types: ['phone', 'email', 'id_card'],
        }),
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const result: GenerateResponse = await response.json()
      setData(result.data)
    } catch (err) {
      setError(err instanceof Error ? err.message : '生成失败，请检查后端服务')
      console.error('Generate error:', err)
    } finally {
      setIsGenerating(false)
    }
  }

  const handleCopy = () => {
    const text = data.map(row => {
      const parts = []
      if (row.phone) parts.push(row.phone)
      if (row.email) parts.push(row.email)
      if (row.id_card) parts.push(row.id_card)
      return parts.join('\t')
    }).join('\n')
    
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleExportCSV = () => {
    const headers = ['手机号', '邮箱', '身份证号']
    const rows = data.map(row => [
      row.phone || '',
      row.email || '',
      row.id_card || '',
    ].join(','))
    
    const csv = headers.join(',') + '\n' + rows.join('\n')
    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `test_data_${Date.now()}.csv`
    a.click()
    URL.revokeObjectURL(url)
  }

  const handleExportJSON = () => {
    const json = JSON.stringify(data.map(row => ({
      '手机号': row.phone || '',
      '邮箱': row.email || '',
      '身份证号': row.id_card || '',
    })), null, 2)
    const blob = new Blob([json], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `test_data_${Date.now()}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="gradient-bg-warm">
      {/* 导航栏 */}
      <nav className="sticky top-0 z-50 backdrop-blur-xl bg-white/70 border-b border-pink-100/50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="icon-container">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold gradient-text">TestData Factory</h1>
                <p className="text-xs text-gray-400">让造数据变得可爱又轻松</p>
              </div>
            </div>

            {/* 导航链接 */}
            <div className="hidden sm:flex items-center gap-6">
              <a href="#features" className="text-sm text-gray-600 hover:text-pink-500 transition-colors">功能</a>
              <a href="#generator" className="text-sm text-gray-600 hover:text-pink-500 transition-colors">生成器</a>
              <a 
                href="http://localhost:8000/docs" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center gap-1.5 text-sm text-gray-600 hover:text-pink-500 transition-colors"
              >
                <Settings className="w-4 h-4" />
                API 文档
              </a>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero 区域 */}
      <section className="relative py-16 sm:py-24 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 badge-soft mb-6">
            <span className="text-sm">✨</span>
            <span>v0.1.0 MVP</span>
          </div>
          
          <h2 className="text-4xl sm:text-5xl font-bold mb-6">
            <span className="gradient-text">智能测试数据</span>
            <br />
            <span className="text-gray-800">一键生成</span>
          </h2>
          
          <p className="text-lg text-gray-500 max-w-2xl mx-auto mb-8">
            手机号、邮箱、身份证号...告别手写 SQL 和复制粘贴，
            <span className="text-pink-500 font-medium">让造数据成为享受</span>
          </p>

          <div className="flex flex-wrap justify-center gap-4">
            <button 
              onClick={() => document.getElementById('generator')?.scrollIntoView({ behavior: 'smooth' })}
              className="btn-primary flex items-center gap-2"
            >
              <Sparkles className="w-4 h-4" />
              立即开始
            </button>
            <a 
              href="http://localhost:8000/docs"
              target="_blank"
              className="btn-secondary flex items-center gap-2"
            >
              <Settings className="w-4 h-4" />
              API 文档
            </a>
          </div>
        </div>
      </section>

      {/* 功能特性 */}
      <section id="features" className="py-12 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="card-clay p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-3 bg-gradient-to-br from-pink-400 to-purple-400 rounded-xl">
                  <Wand2 className="w-5 h-5 text-white" />
                </div>
                <h3 className="font-bold text-gray-800">自定义规则</h3>
              </div>
              <p className="text-sm text-gray-500 leading-relaxed">
                支持正则表达式，自由定义数据格式，满足各种复杂场景
              </p>
              <div className="mt-4 flex items-center text-xs text-pink-500 font-medium">
                即将推出 <ChevronRight className="w-3 h-3 ml-1" />
              </div>
            </div>

            <div className="card-clay p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-3 bg-gradient-to-br from-cyan-400 to-blue-400 rounded-xl">
                  <Database className="w-5 h-5 text-white" />
                </div>
                <h3 className="font-bold text-gray-800">数据库逆向</h3>
              </div>
              <p className="text-sm text-gray-500 leading-relaxed">
                连接数据库，自动识别表结构，智能生成关联数据
              </p>
              <div className="mt-4 flex items-center text-xs text-cyan-500 font-medium">
                Phase 2 <ChevronRight className="w-3 h-3 ml-1" />
              </div>
            </div>

            <div className="card-clay p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-3 bg-gradient-to-br from-purple-400 to-indigo-400 rounded-xl">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <h3 className="font-bold text-gray-800">AI 智能推断</h3>
              </div>
              <p className="text-sm text-gray-500 leading-relaxed">
                输入需求描述，AI 自动推断数据规则，一句话搞定
              </p>
              <div className="mt-4 flex items-center text-xs text-purple-500 font-medium">
                敬请期待 <ChevronRight className="w-3 h-3 ml-1" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 生成器 */}
      <section id="generator" className="py-12 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto">
          {/* 配置卡片 */}
          <div className="card-clay p-6 sm:p-8 mb-6">
            <div className="flex flex-col sm:flex-row items-start sm:items-end gap-4">
              <div className="flex-1 w-full">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  生成数量
                </label>
                <input
                  type="number"
                  value={count}
                  onChange={(e) => setCount(Math.max(1, Math.min(1000, parseInt(e.target.value) || 1)))}
                  min={1}
                  max={1000}
                  className="input-soft text-center text-lg font-semibold"
                />
                <p className="text-xs text-gray-400 mt-1.5">支持 1-1000 条数据</p>
              </div>
              
              <button 
                onClick={handleGenerate}
                disabled={isGenerating}
                className="btn-primary w-full sm:w-auto flex items-center justify-center gap-2 disabled:opacity-70"
              >
                {isGenerating ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    生成中...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    生成数据
                  </>
                )}
              </button>
            </div>

            {/* 错误提示 */}
            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-red-800">生成失败</p>
                  <p className="text-sm text-red-600 mt-1">{error}</p>
                  <p className="text-xs text-red-500 mt-2">
                    请确保后端服务正在运行：<code className="bg-red-100 px-1.5 py-0.5 rounded">uvicorn testdata_factory.api:app --reload --port 8000</code>
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* 结果展示 */}
          {data.length > 0 && (
            <div className="card-clay overflow-hidden">
              {/* 工具栏 */}
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 sm:p-6 border-b border-pink-100/50 bg-gradient-to-r from-pink-50/50 to-purple-50/50">
                <div>
                  <h3 className="font-bold text-gray-800">生成结果</h3>
                  <p className="text-sm text-gray-500 mt-0.5">已生成 {data.length} 条数据</p>
                </div>
                
                <div className="flex flex-wrap gap-2">
                  <button 
                    onClick={handleCopy}
                    className="px-4 py-2 bg-white border border-pink-200 rounded-lg text-sm font-medium text-pink-600 hover:bg-pink-50 transition-colors flex items-center gap-1.5"
                  >
                    {copied ? (
                      <>
                        <Check className="w-4 h-4 text-green-500" />
                        已复制
                      </>
                    ) : (
                      <>
                        <Copy className="w-4 h-4" />
                        复制
                      </>
                    )}
                  </button>
                  <button 
                    onClick={handleExportCSV}
                    className="px-4 py-2 bg-white border border-pink-200 rounded-lg text-sm font-medium text-pink-600 hover:bg-pink-50 transition-colors flex items-center gap-1.5"
                  >
                    <Download className="w-4 h-4" />
                    CSV
                  </button>
                  <button 
                    onClick={handleExportJSON}
                    className="px-4 py-2 bg-white border border-purple-200 rounded-lg text-sm font-medium text-purple-600 hover:bg-purple-50 transition-colors flex items-center gap-1.5"
                  >
                    <Download className="w-4 h-4" />
                    JSON
                  </button>
                </div>
              </div>

              {/* 数据表格 */}
              <div className="overflow-x-auto">
                <table className="table-soft">
                  <thead>
                    <tr>
                      <th>
                        <div className="flex items-center gap-2">
                          <Phone className="w-4 h-4" />
                          手机号
                        </div>
                      </th>
                      <th>
                        <div className="flex items-center gap-2">
                          <Mail className="w-4 h-4" />
                          邮箱
                        </div>
                      </th>
                      <th>
                        <div className="flex items-center gap-2">
                          <CreditCard className="w-4 h-4" />
                          身份证号
                        </div>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.map((row, index) => (
                      <tr key={index}>
                        <td className="font-mono text-sm">{row.phone || '-'}</td>
                        <td className="text-sm">{row.email || '-'}</td>
                        <td className="font-mono text-sm">{row.id_card || '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* 页脚 */}
      <footer className="border-t border-pink-100/50 bg-white/50 py-8 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div className="p-1.5 bg-gradient-to-br from-pink-400 to-purple-400 rounded-lg">
                <Sparkles className="w-4 h-4 text-white" />
              </div>
              <span className="text-sm font-medium text-gray-600">TestData Factory</span>
            </div>
            
            <p className="text-sm text-gray-400">
              Made with <span className="text-pink-400">💖</span> by 知微 & 千机
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
