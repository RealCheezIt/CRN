from flask import Blueprint, render_template, request, redirect, url_for, session
from app import database

from flask import Response
from app.utils.md import note_to_markdown
from app.utils.github import push_to_github

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/note')
def note_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.show_login_page'))
    return render_template('note.html', note=None, note_tags=[])



@notes_bp.route('/save_note', methods=['POST']) # 노트 저장을 눌렀을때 실행 되는 라우트
def save_note(): # 노트 저장 함수
    title = request.form.get('title') # html 파일 내에 form 태그에서 타이틀,
    category = request.form.get('category')# 카테고리,
    content = request.form.get('content')  # 내용 가져오기
    tags_input = request.form.get('tags', '') #newwwwwwww



    user_id = session.get('user_id') # 세션에서 유저 아이디 가져오기 
    if not user_id: # 만약 세션에 유저 아이디가 없으면
        return redirect(url_for('auth.show_login_page'))  # 인증 미들웨어

    database.save_note(user_id, title, category, content)  # 데이터베이스에 저장
    conn_note_id = database.get_last_note_id(user_id)
    tag_names = tags_input.split(',')
    database.save_note_tags(conn_note_id, tag_names)






    return redirect(url_for('notes.show_my_notes'))# 저장 후 내 노트 페이지로 이동

@notes_bp.route('/my_notes') # 내 노트 페이지
def show_my_notes(): # 내 노트 페이지 함수
    if 'user_id' not in session: # 만약 세션에 유저 아이디가 없다면
        return redirect(url_for('auth.show_login_page')) # 인증 미들웨어 3, 로그인 페이지로 안내

    current_user = session.get('user_id') # 현재 유저
    user_notes = database.get_my_notes(current_user) # 그 현재 유저의 노트



    return render_template('my_notes.html', notes=user_notes, user=current_user) # XSS 방지 부분 # # 내 노트 리스트에 위에서 선언 해뒀던 현재 유저와 현재 유저의 노트 같이 렌더링

@notes_bp.route('/note/<int:note_id>/export')
def export_note(note_id):
    note = database.get_note_by_id(note_id)
    md_content = note_to_markdown(note)
    return Response(
        md_content,
        mimetype='text/markdown',
        headers={'Content-Disposition': f'attachment; filename=note_{note_id}.md'}
    )



@notes_bp.route('/note/<int:note_id>/push_github', methods=['POST'])
def push_github(note_id):
    note = database.get_note_by_id(note_id)
    success = push_to_github(note)
    return redirect(url_for('notes.show_my_notes'))



@notes_bp.route('/note/<int:note_id>/edit', methods=['GET', 'POST'])
def edit_note(note_id):
    # 인증 미들웨어
    if 'user_id' not in session:
        return redirect(url_for('auth.show_login_page'))

    user_id = session.get('user_id')
    # 수정 완료 버튼 눌러서 데이터 전송 [POST]
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        content = request.form.get('content')
        tags_input = request.form.get('tags', '')  # oh yeah new one

        database.update_note(note_id, user_id, title, category, content)  
        database.clear_note_tags(note_id)
        database.save_note_tags(note_id, tags_input.split(','))
        



        # 내용 수정
        database.update_note(note_id, user_id, title, category, content)
        return redirect(url_for('notes.show_my_notes'))

    # GET일 땐 기존 값 채워서 폼 보여주기
    note = database.get_note_by_id(note_id)
    note_tags = database.get_tags_for_note(note_id)
    return render_template('note.html', note=note, tags=note_tags)


@notes_bp.route('/note/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.show_login_page'))
    user_id = session.get('user_id')
    database.delete_note(note_id, user_id)
    return redirect(url_for('notes.show_my_notes'))


@notes_bp.route('/my_notes')
def show_my_notes():
    if 'user_id' not in session:
        return redirect(url_for('auth.show_login_page'))
    current_user = session.get('user_id')
    user_notes = database.get_my_notes(current_user)
    notes_with_tags = [(note, database.get_tags_for_note(note[0])) for note in user_notes]
    return render_template('my_notes.html', notes=notes_with_tags, user=current_user)


