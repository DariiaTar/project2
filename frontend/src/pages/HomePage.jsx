import React from 'react';
import { Link } from 'react-router-dom';

const categories = [
  { key: 'tennis', icon: '🎾', label: 'Теніс', desc: 'Тенісні корти з різним покриттям' },
  { key: 'football', icon: '⚽', label: 'Футбол', desc: 'Поля зі штучним та натуральним газоном' },
  { key: 'pool', icon: '🏊', label: 'Басейн', desc: 'Олімпійські та тренувальні басейни' },
  { key: 'gym', icon: '🏋️', label: 'Тренажерний зал', desc: 'Сучасне обладнання для тренувань' },
];

export default function HomePage() {
  return (
    <div>
      {/* Hero */}
      <div style={{
        background: 'linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%)',
        borderRadius: '20px',
        padding: '64px 48px',
        textAlign: 'center',
        marginBottom: '48px',
        position: 'relative',
        overflow: 'hidden',
      }}>
        <div style={{ position: 'absolute', top: '-50px', right: '-50px', fontSize: '200px', opacity: 0.05 }}>🏟️</div>
        <h1 style={{ color: '#fff', fontSize: '42px', fontWeight: 800, margin: '0 0 16px', lineHeight: 1.2 }}>
          Бронюйте спортивні<br />
          <span style={{ color: '#e94560' }}>локації онлайн</span>
        </h1>
        <p style={{ color: '#aaa', fontSize: '18px', margin: '0 0 32px', maxWidth: '500px', marginLeft: 'auto', marginRight: 'auto' }}>
          Тенісні корти, футбольні поля, басейни та тренажерні зали — все в одному місці
        </p>
        <Link to="/locations" style={{
          background: '#e94560',
          color: '#fff',
          padding: '14px 32px',
          borderRadius: '12px',
          textDecoration: 'none',
          fontWeight: 700,
          fontSize: '16px',
          display: 'inline-block',
        }}>
          Переглянути локації →
        </Link>
      </div>

      {/* Categories */}
      <h2 style={{ fontSize: '24px', fontWeight: 800, color: '#1a1a2e', marginBottom: '20px' }}>
        Категорії локацій
      </h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '16px', marginBottom: '48px' }}>
        {categories.map((cat) => (
          <Link key={cat.key} to={`/locations?category=${cat.key}`} style={{
            background: '#fff',
            borderRadius: '16px',
            padding: '24px',
            textDecoration: 'none',
            boxShadow: '0 2px 12px rgba(0,0,0,0.06)',
            transition: 'transform 0.2s, box-shadow 0.2s',
            display: 'block',
          }}
          onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-4px)'; e.currentTarget.style.boxShadow = '0 8px 24px rgba(0,0,0,0.12)'; }}
          onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = '0 2px 12px rgba(0,0,0,0.06)'; }}>
            <div style={{ fontSize: '40px', marginBottom: '12px' }}>{cat.icon}</div>
            <div style={{ fontWeight: 700, color: '#1a1a2e', fontSize: '16px', marginBottom: '6px' }}>{cat.label}</div>
            <div style={{ color: '#888', fontSize: '13px' }}>{cat.desc}</div>
          </Link>
        ))}
      </div>

      {/* How it works */}
      <div style={{ background: '#fff', borderRadius: '20px', padding: '40px', boxShadow: '0 2px 12px rgba(0,0,0,0.06)' }}>
        <h2 style={{ fontSize: '24px', fontWeight: 800, color: '#1a1a2e', marginBottom: '24px', textAlign: 'center' }}>
          Як це працює?
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '24px' }}>
          {[
            { step: '1', icon: '🔍', title: 'Оберіть локацію', desc: 'Перегляньте доступні спортивні локації та оберіть зручну' },
            { step: '2', icon: '📅', title: 'Оберіть час', desc: 'Виберіть зручний слот з доступних варіантів' },
            { step: '3', icon: '✅', title: 'Забронюйте', desc: 'Підтвердіть бронювання та очікуйте підтвердження' },
          ].map(item => (
            <div key={item.step} style={{ textAlign: 'center' }}>
              <div style={{
                width: '56px', height: '56px', background: '#e94560',
                borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center',
                margin: '0 auto 12px', fontSize: '24px',
              }}>
                {item.icon}
              </div>
              <div style={{ fontWeight: 700, color: '#1a1a2e', marginBottom: '8px' }}>{item.title}</div>
              <div style={{ color: '#888', fontSize: '13px', lineHeight: 1.5 }}>{item.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
